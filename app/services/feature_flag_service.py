"""Feature flag service for controlling feature visibility by role."""

import logging
from flask import g, has_request_context
from app import db
from app.models import FeatureFlag, FeatureFlagAuditLog

logger = logging.getLogger(__name__)

# Valid role values (must match Member.role)
VALID_ROLES = ['member', 'teamster', 'administrator']


def _get_request_cache():
    """Get request-scoped cache, creating if necessary."""
    if not has_request_context():
        return None
    if not hasattr(g, '_feature_flags_cache'):
        g._feature_flags_cache = {}
    return g._feature_flags_cache


class FeatureFlagService:
    """Service for managing feature flags."""

    @staticmethod
    def get_all_flags() -> list:
        """Get all feature flags. Uses request-scoped caching."""
        cache = _get_request_cache()
        cache_key = 'all_flags'

        if cache is not None and cache_key in cache:
            return cache[cache_key]

        flags = FeatureFlag.query.order_by(FeatureFlag.name).all()

        if cache is not None:
            cache[cache_key] = flags

        return flags

    @staticmethod
    def is_enabled_for_user(flag_key: str, user) -> bool:
        """
        Check if feature is enabled for user.
        Returns True if flag is missing (graceful fallback with warning).
        """
        cache = _get_request_cache()
        cache_key = f'flag_{flag_key}'

        # Check cache first
        if cache is not None and cache_key in cache:
            flag = cache[cache_key]
        else:
            flag = FeatureFlag.query.filter_by(key=flag_key).first()
            if cache is not None:
                cache[cache_key] = flag

        # Graceful fallback: missing flag = enabled for all
        if flag is None:
            logger.warning(f"Feature flag '{flag_key}' not found, defaulting to enabled")
            return True

        # Disabled = blocked for everyone
        if not flag.is_enabled:
            return False

        # No role restriction = enabled for all
        if not flag.allowed_roles:
            return True

        # Check user role
        return user.role in flag.allowed_roles

    @staticmethod
    def update_flag(flag_id: int, is_enabled: bool, allowed_roles: list, admin_id: str):
        """Update flag settings and log audit entry. Returns (success, error)."""
        try:
            flag = FeatureFlag.query.get(flag_id)
            if not flag:
                return False, 'Feature-Flag nicht gefunden'

            # Validate roles
            if allowed_roles:
                invalid_roles = [r for r in allowed_roles if r not in VALID_ROLES]
                if invalid_roles:
                    return False, f'Ungültige Rollen: {", ".join(invalid_roles)}'

            # Track changes
            changes = {}
            if flag.is_enabled != is_enabled:
                changes['is_enabled'] = {'old': flag.is_enabled, 'new': is_enabled}

            old_roles = flag.allowed_roles or []
            new_roles = allowed_roles or []
            if set(old_roles) != set(new_roles):
                changes['allowed_roles'] = {'old': old_roles, 'new': new_roles}

            if not changes:
                return True, None  # No changes

            # Apply changes
            flag.is_enabled = is_enabled
            flag.allowed_roles = allowed_roles if allowed_roles else None

            # Create audit log
            audit_log = FeatureFlagAuditLog(
                flag_id=flag.id,
                flag_key=flag.key,
                operation='update',
                operation_data={
                    'flag_name': flag.name,
                    'changes': changes
                },
                performed_by_id=admin_id
            )
            db.session.add(audit_log)
            db.session.commit()

            # Clear cache
            cache = _get_request_cache()
            if cache is not None:
                cache.clear()

            return True, None

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating feature flag: {e}")
            return False, 'Fehler beim Aktualisieren des Feature-Flags'
