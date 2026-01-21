# Feature Flags System Implementation Plan

## Overview
Add a feature flags system to the admin panel allowing admins to activate/deactivate predefined features and control visibility based on user roles. Flags are defined by developers in migrations; admins toggle them via a simple UI.

**Initial use case:** Restrict Help Center to admins only during content review.

## Design Principles (per CLAUDE.md)

- **KISS**: Simple toggle UI, no CRUD for flag creation
- **SOLID/DRY**: Reuse existing patterns (SettingsService caching, audit log structure)
- **Never break existing functionality**: Additive changes only, feature flags default to "enabled for all" if missing
- **German UI**: All labels in German
- **Audit completeness**: Full audit trail with human-readable details

## Database Schema

### New Model: `FeatureFlag`
```python
class FeatureFlag(db.Model):
    __tablename__ = 'feature_flag'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)  # German display name
    description = db.Column(db.String(255), nullable=True)
    is_enabled = db.Column(db.Boolean, nullable=False, default=True)
    allowed_roles = db.Column(db.JSON, nullable=True)  # null = all roles when enabled
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

### New Model: `FeatureFlagAuditLog`
```python
class FeatureFlagAuditLog(db.Model):
    __tablename__ = 'feature_flag_audit_log'

    id = db.Column(db.Integer, primary_key=True)
    flag_id = db.Column(db.Integer, nullable=False)
    flag_key = db.Column(db.String(50), nullable=False)  # Denormalized for readability
    operation = db.Column(db.String(20), nullable=False)  # 'update'
    operation_data = db.Column(db.JSON, nullable=True)  # {old_values, new_values}
    performed_by_id = db.Column(db.String(36), db.ForeignKey('member.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

### Role Logic
| `is_enabled` | `allowed_roles` | Result |
|--------------|-----------------|--------|
| `False` | any | Disabled for everyone |
| `True` | `null` | Enabled for all authenticated users |
| `True` | `['administrator']` | Admin only |
| `True` | `['administrator', 'teamster']` | Admin + Teamster |

### Graceful Fallback
If a feature flag key doesn't exist in DB → treat as **enabled for all** (safe default, doesn't break existing features).

## Implementation Steps

### 1. Database Models
**File:** `app/models.py`
- Add `FeatureFlag` model after `SystemSetting` (~line 609)
- Add `FeatureFlagAuditLog` model after other audit logs

### 2. Database Migration
```bash
source .venv/bin/activate && flask db migrate -m "Add feature flags"
source .venv/bin/activate && flask db upgrade
```

### 3. Seed Initial Flag (in migration)
```python
# In migration upgrade():
from app.models import FeatureFlag
flag = FeatureFlag(
    key='help_center',
    name='Hilfe-Center',
    description='Hilfe-Seiten für Mitglieder',
    is_enabled=True,
    allowed_roles=['administrator']  # Admin-only during review
)
db.session.add(flag)
db.session.commit()
```

### 4. Feature Flag Service
**New file:** `app/services/feature_flag_service.py`

Following `SettingsService` pattern:
```python
class FeatureFlagService:
    @staticmethod
    def get_all_flags() -> dict:
        """Get all flags as dict keyed by key. Request-scoped caching."""

    @staticmethod
    def is_enabled_for_user(flag_key: str, user) -> bool:
        """Check if feature enabled for user. Returns True if flag missing (safe default)."""

    @staticmethod
    def update_flag(flag_id: int, is_enabled: bool, allowed_roles: list, admin_id: str):
        """Update flag and log change."""
```

### 5. Route Protection Decorator
**File:** `app/decorators/auth.py`

```python
def feature_required(flag_key):
    """Require feature flag enabled for current user. Returns 404 if disabled."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return f(*args, **kwargs)  # Let @login_required handle

            if not FeatureFlagService.is_enabled_for_user(flag_key, current_user):
                abort(404)  # Pretend page doesn't exist
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### 6. Template Context Processor
**File:** `app/__init__.py`

```python
@app.context_processor
def inject_feature_flags():
    def is_feature_enabled(flag_key):
        if not current_user.is_authenticated:
            return False
        return FeatureFlagService.is_enabled_for_user(flag_key, current_user)
    return {'is_feature_enabled': is_feature_enabled}
```

### 7. Admin API Endpoints (simplified - update only)
**File:** `app/routes/api/admin.py`

- `GET /api/admin/feature-flags` - List all flags
- `PUT /api/admin/feature-flags/<id>` - Update flag (toggle + roles)

No POST/DELETE - flags are predefined in migrations.

### 8. Admin Page Route
**File:** `app/routes/admin/views.py`

```python
@bp.route('/feature-flags')
@login_required
@admin_required
def feature_flags():
    """Feature flags management page."""
    return render_template('admin/feature_flags.html')
```

### 9. Admin UI Template (Simple Toggle List)
**New file:** `app/templates/admin/feature_flags.html`

Simple table with:
- Flag name + description
- Toggle switch for enabled/disabled
- Checkboxes for roles (Mitglied, Platzbetreuer, Administrator)
- Auto-save on change (no submit button needed)

No create/edit/delete modals - just inline controls.

### 10. Navigation Updates
**File:** `app/templates/base.html`

Desktop menu (line ~143):
```jinja2
{% if is_feature_enabled('help_center') %}
<a href="{{ url_for('members.help_center') }}" class="...">
    <span class="material-icons text-sm">help_outline</span>
    <span>Hilfe</span>
</a>
{% endif %}
```

Mobile menu: Same pattern for the Help link there.

Admin dropdown: Add "Feature-Flags" link.

### 11. Admin Overview Card
**File:** `app/templates/admin/overview.html`

Add card linking to feature flags page.

### 12. Apply to Help Center Route
**File:** `app/routes/members.py`

```python
@bp.route('/help', methods=['GET'])
@bp.route('/help/<path:article>', methods=['GET'])
@login_required
@feature_required('help_center')  # Add this
def help_center(article=None):
    ...
```

### 13. Audit Log Integration (per CLAUDE.md rules)
**File:** `app/routes/admin/audit.py`
- Add `format_feature_flag_details()` function

**File:** `app/templates/admin/audit_log.html`
- Add to `valid_operations`: `update` for feature flags
- Add German label: `'update': 'Aktualisiert'`
- Add field labels: `flag_name`, `is_enabled`, `allowed_roles`
- Add formatting for role arrays → German role names

## Files Summary

| File | Action | Risk |
|------|--------|------|
| `app/models.py` | Add 2 models | Low |
| `app/services/feature_flag_service.py` | Create | Low |
| `app/decorators/auth.py` | Add decorator | Low |
| `app/__init__.py` | Add context processor | Low |
| `app/routes/api/admin.py` | Add 2 endpoints | Low |
| `app/routes/admin/views.py` | Add 1 route | Low |
| `app/templates/admin/feature_flags.html` | Create | Low |
| `app/templates/admin/overview.html` | Add 1 card | Low |
| `app/templates/base.html` | Wrap menu items | Medium |
| `app/routes/members.py` | Add decorator | Low |
| `app/routes/admin/audit.py` | Add formatting | Low |
| `app/templates/admin/audit_log.html` | Add labels | Low |

## Safety Measures

1. **Graceful fallback**: Missing flag → enabled for all (no breakage)
2. **Additive only**: No existing code removed, only wrapped
3. **Tests first**: Run full test suite before and after each step
4. **Template changes isolated**: Only Help Center link affected initially

## Verification Plan

1. **Run tests**: `source .venv/bin/activate && pytest`
2. **Start dev server**: `source .venv/bin/activate && flask run --debug`
3. **Test as admin** (login as admin user):
   - Navigate to Admin → Feature-Flags
   - Verify Help Center flag shows with admin-only role
   - Toggle enabled/disabled, verify immediate effect
   - Check audit log for change entry
4. **Test as regular member** (login as max@tcz.at):
   - Verify Help Center menu item is hidden
   - Navigate directly to `/members/help` → should show 404 page
5. **Test enabling for all**:
   - As admin, set allowed_roles to empty (all users)
   - Verify Help Center visible for regular members
6. **Run tests again**: `source .venv/bin/activate && pytest`
