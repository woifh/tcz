"""Settings service for managing system-wide settings."""
from datetime import date
import logging
from app import db
from app.models import SystemSetting

logger = logging.getLogger(__name__)


class SettingsService:
    """Service for managing system settings stored in SystemSetting model."""

    PAYMENT_DEADLINE_KEY = 'payment_deadline_date'

    @staticmethod
    def get_payment_deadline():
        """
        Get the configured payment deadline date.

        Returns:
            date | None: The deadline date, or None if not set
        """
        try:
            setting = SystemSetting.query.filter_by(key=SettingsService.PAYMENT_DEADLINE_KEY).first()
            if setting and setting.value:
                return date.fromisoformat(setting.value)
            return None
        except (ValueError, Exception) as e:
            logger.error(f"Error getting payment deadline: {e}")
            return None

    @staticmethod
    def set_payment_deadline(deadline_date, admin_id=None):
        """
        Set the payment deadline date.

        Args:
            deadline_date: The deadline date (date object or ISO string)
            admin_id: ID of admin setting the deadline (for logging)

        Returns:
            tuple: (success: bool, error_message: str | None)
        """
        try:
            # Convert to date if string
            if isinstance(deadline_date, str):
                deadline_date = date.fromisoformat(deadline_date)

            # Get or create the setting
            setting = SystemSetting.query.filter_by(key=SettingsService.PAYMENT_DEADLINE_KEY).first()

            if setting:
                setting.value = deadline_date.isoformat()
            else:
                setting = SystemSetting(
                    key=SettingsService.PAYMENT_DEADLINE_KEY,
                    value=deadline_date.isoformat()
                )
                db.session.add(setting)

            db.session.commit()

            logger.info(f"Payment deadline set to {deadline_date} by admin {admin_id}")
            return True, None

        except ValueError as e:
            logger.error(f"Invalid date format for payment deadline: {e}")
            return False, "Ungültiges Datumsformat"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error setting payment deadline: {e}")
            return False, f"Fehler beim Speichern der Zahlungsfrist: {str(e)}"

    @staticmethod
    def clear_payment_deadline(admin_id=None):
        """
        Remove the payment deadline.

        Args:
            admin_id: ID of admin clearing the deadline (for logging)

        Returns:
            tuple: (success: bool, error_message: str | None)
        """
        try:
            setting = SystemSetting.query.filter_by(key=SettingsService.PAYMENT_DEADLINE_KEY).first()

            if setting:
                db.session.delete(setting)
                db.session.commit()
                logger.info(f"Payment deadline cleared by admin {admin_id}")

            return True, None

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error clearing payment deadline: {e}")
            return False, f"Fehler beim Entfernen der Zahlungsfrist: {str(e)}"

    @staticmethod
    def is_past_payment_deadline():
        """
        Check if the current date is past the payment deadline.

        Returns:
            bool: True if past deadline, False otherwise (including if no deadline set)
        """
        deadline = SettingsService.get_payment_deadline()
        if deadline is None:
            return False  # No deadline means no restriction
        return date.today() > deadline

    @staticmethod
    def days_until_deadline():
        """
        Get the number of days until the payment deadline.

        Returns:
            int | None: Number of days until deadline (negative if past), None if no deadline set
        """
        deadline = SettingsService.get_payment_deadline()
        if deadline is None:
            return None
        delta = deadline - date.today()
        return delta.days

    @staticmethod
    def get_unpaid_member_count():
        """
        Get the count of members who have not paid their fee.

        Returns:
            int: Count of unpaid members
        """
        from app.models import Member
        return Member.query.filter(
            Member.fee_paid == False,
            Member.is_active == True,
            Member.membership_type == 'full'
        ).count()
