# CLAUDE.md

## ⛔ CRITICAL RULES — NEVER VIOLATE

These rules are **NON-NEGOTIABLE**. Violating them is a serious error.

### Git Rules

1. **NEVER commit or push** unless the user explicitly requests it.
   - ✅ Permission phrases: "push", "commit", "push to GitHub", "commit and push"
   - ❌ NOT permission: "looks good", "that's fine", "ship it", "done", "perfect"

2. **When pushing (only after explicit request):**
   - Ask user: major or minor version bump?
   - Draft a short, non-technical changelog entry
   - **SHOW the changelog to the user and WAIT for approval**
   - Only after approval: commit, push, create git tag
   - Version format: Changelog "3.10" → git tag "v3.10.0" (must always match)

### Production Rules

3. **NEVER touch production (PythonAnywhere)** without explicit user request.
   - No file uploads
   - No webapp reloads
   - No MCP tools that affect production
   - No scheduled tasks

### Content Rules

4. **NEVER mention Claude, AI, or Claude Code** in commits, changelogs, comments, or any project files.

### Code Quality Rules

5. **NEVER break existing functionality** — preserve working behavior at all costs. If a change might affect existing features, verify they still work before proceeding.

### STOP AND ASK Before:

- Any `git commit` or `git push`
- Any MCP tool that touches production
- Deleting any file
- Running database migrations on production
- Any destructive or irreversible action
- When in doubt about anything — ask, don't guess

---

## 🧠 How to Work With Me (Vibe Coding Style)

### Think Before You Code

Before writing any code, take a moment to:
1. **Understand the goal** — What problem are we actually solving?
2. **Identify the minimal change** — What's the smallest modification that achieves this?
3. **Consider side effects** — What else might this touch? Check for dependencies.
4. **Plan verification** — How will we know it works?

If the task is ambiguous, ask a clarifying question BEFORE starting. One good question beats three wrong attempts.

### Work Incrementally

- **Small steps**: Make one logical change at a time
- **Verify often**: Run tests after meaningful changes, not just at the end
- **Show progress**: For multi-step tasks, briefly confirm after each step
- **Pause at decision points**: If there are multiple valid approaches, present options

### Communication Style

- **Be concise**: Skip preamble. Get to the point.
- **No fluff**: Don't explain what you're "about to do" — just do it
- **Announce risks**: If something might break, say so BEFORE doing it
- **Summarize changes**: After edits, briefly list what changed (files, functions)
- **Ask, don't assume**: When requirements are unclear, ask one focused question

### When Things Go Wrong

If tests fail or something breaks:
1. **STOP** — Don't pile on more changes
2. **Diagnose** — Read the error carefully, identify root cause
3. **Explain** — Tell me what broke and why, in plain language
4. **Propose fix** — Suggest the minimal fix, wait for approval if uncertain
5. **Verify** — Run tests again to confirm the fix worked

If you're stuck or unsure, say so. "I'm not sure how to approach this" is a valid response.

### Scope Control

- **Do what's asked** — Not more, not less
- **Resist gold-plating** — Don't add features, improvements, or refactors I didn't request
- **Flag scope creep** — If you notice the task growing, pause and check in
- **One thing at a time** — Finish the current task before suggesting the next

### Code Style Preferences

- **Match existing patterns** — Look at nearby code and follow its style
- **Boring is good** — Prefer obvious, straightforward solutions
- **No premature abstraction** — Duplicate a little before extracting
- **Explicit over implicit** — Clear is better than clever
- **Names matter** — Spend time on good names; they're documentation

---

## ✅ Testing Workflow

### When to Run Tests

- **After every meaningful code change** — Don't wait until the end
- **Before declaring a task complete** — Always verify
- **After fixing a bug** — Confirm it's actually fixed
- **When touching shared code** — Services, models, utilities

### Test Commands

```bash
# Run all tests (default choice)
source .venv/bin/activate && pytest

# Run specific test file (when working on one area)
source .venv/bin/activate && pytest tests/test_reservations.py -v

# Run with coverage (before major releases)
source .venv/bin/activate && pytest --cov=app --cov-report=html
```

### If Tests Fail

1. Read the failure message carefully
2. Identify if it's a real bug or a test that needs updating
3. Fix the root cause, not the symptom
4. Run tests again to confirm
5. Tell me what was wrong and how you fixed it

---

## 🏗️ Project Architecture

This is a Flask web application for tennis court reservation management (TCZ - Tennis Club Zellerndorf).

### Backend Structure

- **Factory pattern**: App created via `create_app()` in `app/__init__.py`
- **Blueprints**: Routes organized by domain in `app/routes/`
  - `auth.py` - Authentication (login, logout, password reset)
  - `courts.py` - Court availability views
  - `reservations.py` - Booking management
  - `members.py` - Member management
  - `admin.py` - Admin dashboard
  - `api/` - REST API endpoints (mobile app support)
- **Service layer**: Business logic in `app/services/`
  - `reservation_service.py` - Booking rules, validation
  - `member_service.py` - Member CRUD operations
  - `block_service.py` - Court blocking logic
  - `notification_service.py` - Email notifications
- **Models**: SQLAlchemy models in `app/models/`

### Where to Put Things

| Type of code | Location | Example |
|--------------|----------|---------|
| Business logic | `app/services/` | Validation rules, calculations |
| Database queries | `app/models/` or services | Complex queries in services |
| Route handlers | `app/routes/` | Thin controllers, delegate to services |
| Reusable utilities | `app/utils/` | Date formatting, timezone handling |
| Constants/config | `app/constants/` | Booking limits, time windows |
| Frontend components | `app/static/js/components/` | Alpine.js components |

### Code Patterns to Follow

```python
# ✅ GOOD: Thin route, logic in service
@bp.route('/reservations', methods=['POST'])
@login_required
def create_reservation():
    result = reservation_service.create(current_user, request.json)
    if result.error:
        return jsonify(error=result.error), 400
    return jsonify(result.data), 201

# ❌ BAD: Business logic in route
@bp.route('/reservations', methods=['POST'])
@login_required
def create_reservation():
    # 50 lines of validation and database calls here...
```

```python
# ✅ GOOD: Explicit error handling
def get_member(member_id):
    member = Member.query.get(member_id)
    if not member:
        raise MemberNotFoundError(f"Member {member_id} not found")
    return member

# ❌ BAD: Silent failure
def get_member(member_id):
    return Member.query.get(member_id)  # Returns None silently
```

### Frontend Structure

- **Alpine.js**: Client-side reactivity (no build step for JS)
- **Tailwind CSS**: Utility-first styling
- **Components**: `app/static/js/components/`

### API Pattern

All API endpoints use `/api/` prefix:
```javascript
fetch('/api/reservations/...', { ... })
fetch('/api/members/...', { ... })
fetch('/api/courts/availability', { ... })
```

### Authentication

- Session-based auth for web (Flask-Login)
- JWT Bearer tokens for mobile app API access
- Decorator `@jwt_or_session_required` supports both

---

## 🗄️ Database

- SQLite for development (`instance/app.db`)
- MySQL for production (PythonAnywhere)
- Migrations via Flask-Migrate

### Migration Workflow

```bash
# After changing models
source .venv/bin/activate && flask db migrate -m "Description of change"

# Review the generated migration in migrations/versions/
# Then apply it:
source .venv/bin/activate && flask db upgrade
```

⚠️ **Always review generated migrations before applying** — they can be wrong.

---

## 🧪 Testing

- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- Property-based tests using Hypothesis in `tests/property/`
- Fixtures in `tests/conftest.py`

### Local Development Login

For manual testing:
- **User**: max@tcz.at
- **Password**: max@tcz.at

---

## 🚀 Deployment

### Production Environment (PythonAnywhere)

| Setting | Value |
|---------|-------|
| Domain | woifh.pythonanywhere.com |
| Python Version | 3.10 |
| Virtualenv | `/home/woifh/.virtualenvs/tennisclub` |
| Project Path | `/home/woifh/tcz` |

### Production Commands (PythonAnywhere Console)

```bash
# Activate virtualenv (REQUIRED first)
source ~/.virtualenvs/tennisclub/bin/activate

# Full deployment (pull + migrate + reload)
cd /home/woifh/tcz && git pull origin main && flask db upgrade
# Then reload webapp via MCP or dashboard
```

### MCP Tools

```
mcp__pythonanywhere__reload_webapp with domain="woifh.pythonanywhere.com"
mcp__pythonanywhere__read_file_or_directory with path="/home/woifh/tcz/..."
```

---

## 🇩🇪 German Language

UI text is in German:
- Platz = Court
- Sperrung = Block (court blocking)
- Buchung = Booking/Reservation
- Mitglied = Member

---

## 📋 Audit Log Checklist

When adding new audit log operations:

1. ☐ Add operation to `valid_operations` in `app/models.py`
2. ☐ Add German label in `app/templates/admin/audit_log.html` (actionMap)
3. ☐ Add field labels in `app/templates/admin/audit_log.html` (fieldLabels)
4. ☐ Add formatting in `formatDetails()` if needed

### Required Details by Type

| Type | Required fields |
|------|-----------------|
| Reservations | member name, court, date, time |
| Blocks | court(s), date, time range, reason |
| Members | name, changed fields with old/new values |

**Never show raw IDs** — always resolve to human-readable names.

---

## 🔧 Build Commands Reference

```bash
# Python (always activate venv first)
source .venv/bin/activate && pytest              # Run tests
source .venv/bin/activate && flask run --debug   # Dev server
source .venv/bin/activate && flask db migrate    # Create migration
source .venv/bin/activate && flask db upgrade    # Apply migration

# JavaScript
npm run lint          # ESLint
npm run format        # Prettier

# CSS
npm run build:css     # Build Tailwind
npm run watch:css     # Watch mode
```

---

## 📚 Key Files Quick Reference

| File | Purpose |
|------|---------|
| `config.py` | Environment configuration |
| `app/__init__.py` | App factory (`create_app()`) |
| `app/constants/` | Business rules, limits |
| `app/decorators/auth.py` | Auth decorators |
| `app/utils/timezone_utils.py` | Berlin timezone handling |
| `tests/conftest.py` | Test fixtures |
