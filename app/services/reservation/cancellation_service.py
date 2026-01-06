"""Service for cancelling reservations."""
import logging

from app import db
from app.models import Reservation
from app.services.validation_service import ValidationService
from app.services.email_service import EmailService

# Configure logging
logger = logging.getLogger(__name__)


class ReservationCancellationService:
    """Service for cancelling reservations."""

    @staticmethod
    def cancel_reservation(reservation_id, reason=None):
        """
        Cancel a reservation.
        Uses enhanced validation that prevents cancellation within 15 minutes of start time,
        once the slot has started, or for short notice bookings.

        Args:
            reservation_id: ID of the reservation
            reason: Optional cancellation reason

        Returns:
            tuple: (success boolean, error message or None)
        """
        # Use the enhanced validation service
        is_allowed, error_msg = ValidationService.validate_cancellation_allowed(reservation_id)

        if not is_allowed:
            return False, error_msg

        reservation = Reservation.query.get(reservation_id)
        reservation.status = 'cancelled'
        if reason:
            reservation.reason = reason

        try:
            db.session.commit()

            # Send email notifications
            EmailService.send_booking_cancelled(reservation, reason)

            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"Fehler beim Stornieren der Buchung: {str(e)}"
