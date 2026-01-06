"""User role constants for the Tennis Club application."""


class UserRole:
    """Constants for user roles in the system."""

    MEMBER = 'member'
    TEAMSTER = 'teamster'
    ADMINISTRATOR = 'administrator'

    @classmethod
    def all_roles(cls):
        """Return list of all valid roles."""
        return [cls.MEMBER, cls.TEAMSTER, cls.ADMINISTRATOR]

    @classmethod
    def is_valid(cls, role):
        """Check if a role is valid."""
        return role in cls.all_roles()
