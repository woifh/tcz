"""Membership type constants for the Tennis Club application."""


class MembershipType:
    """Constants for membership types in the system."""

    FULL = 'full'
    SUSTAINING = 'sustaining'

    # German labels for UI
    LABELS = {
        'full': 'Vollmitglied',
        'sustaining': 'Fördermitglied'
    }

    @classmethod
    def all_types(cls):
        """Return list of all valid membership types."""
        return [cls.FULL, cls.SUSTAINING]

    @classmethod
    def is_valid(cls, membership_type):
        """Check if a membership type is valid."""
        return membership_type in cls.all_types()

    @classmethod
    def get_label(cls, membership_type):
        """Get German label for membership type."""
        return cls.LABELS.get(membership_type, membership_type)
