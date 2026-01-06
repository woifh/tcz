"""Helper functions for reservation classification and validation."""
import logging
from datetime import time, timedelta, datetime

from app.utils.timezone_utils import ensure_berlin_timezone, log_timezone_operation
from app.utils.error_handling import log_error_with_context, monitor_performance

# Configure logging
logger = logging.getLogger(__name__)


class ReservationHelpers:
    """Helper methods for reservation classification and time-based logic."""

    @staticmethod
    @monitor_performance("is_reservation_active_by_time", threshold_ms=100)
    def is_reservation_active_by_time(reservation_date, reservation_end_time, current_time=None):
        """
        Determine if a reservation is active based on current time.

        A reservation is considered active if:
        - It's on a future date, OR
        - It's on the same date but hasn't ended yet (end_time > current_time)

        This implements the core time-based logic for active booking sessions,
        replacing the previous date-only approach.

        Args:
            reservation_date: Date of the reservation (date object)
            reservation_end_time: End time of the reservation (time object)
            current_time: Current datetime (defaults to Europe/Berlin timezone)

        Returns:
            bool: True if reservation is active (future or in progress)
        """
        try:
            # Ensure consistent Europe/Berlin timezone handling
            berlin_time = ensure_berlin_timezone(current_time)
            log_timezone_operation("is_reservation_active_by_time", current_time, berlin_time)

            current_date = berlin_time.date()
            current_time_only = berlin_time.time()

            # Future reservation (date > current_date): Always active
            if reservation_date > current_date:
                return True

            # Past reservation (date < current_date): Never active
            elif reservation_date < current_date:
                return False

            # Same day reservation: Active if end_time > current_time
            else:  # reservation_date == current_date
                # Handle edge case: if current time exactly matches end time, reservation is NOT active
                return reservation_end_time > current_time_only

        except Exception as e:
            context = {
                'reservation_date': reservation_date,
                'reservation_end_time': reservation_end_time,
                'current_time': current_time
            }
            log_error_with_context(e, context, "is_reservation_active_by_time")

            # Fallback to date-based logic if time calculations fail
            try:
                logger.warning("Falling back to date-based logic for is_reservation_active_by_time")
                fallback_time = ensure_berlin_timezone(None)  # Get current Berlin time
                return reservation_date >= fallback_time.date()
            except Exception as fallback_error:
                log_error_with_context(fallback_error, context, "is_reservation_active_by_time_fallback")
                # Ultimate fallback: assume reservation is active to be safe
                logger.error("Ultimate fallback: assuming reservation is active")
                return True

    @staticmethod
    def is_reservation_currently_active(reservation, current_time=None):
        """
        Check if a reservation object is currently active based on time.

        This is a convenience wrapper around is_reservation_active_by_time()
        that works directly with Reservation model objects.

        Args:
            reservation: Reservation object
            current_time: Current datetime (defaults to Europe/Berlin now)

        Returns:
            bool: True if reservation is active (future or in progress)
        """
        return ReservationHelpers.is_reservation_active_by_time(
            reservation.date,
            reservation.end_time,
            current_time
        )

    @staticmethod
    def is_short_notice_booking(date, start_time, current_time=None):
        """
        Check if a booking would be classified as short notice.

        A booking is short notice if:
        - Current time is within the booking slot (ongoing), OR
        - Current time is within 15 minutes before the slot start

        Args:
            date: Reservation date (assumed to be in Europe/Berlin timezone)
            start_time: Reservation start time (assumed to be in Europe/Berlin timezone)
            current_time: Current datetime (defaults to Europe/Berlin now)

        Returns:
            bool: True if booking is short notice (ongoing or within 15 minutes of start)
        """
        try:
            # Ensure consistent Europe/Berlin timezone handling
            berlin_time = ensure_berlin_timezone(current_time)
            log_timezone_operation("is_short_notice_booking", current_time, berlin_time)

            # Ensure we're comparing like with like - both should be naive datetimes
            # representing the same timezone (Europe/Berlin)
            reservation_start = datetime.combine(date, start_time)

            # Calculate end time (slots are 1 hour long)
            end_hour = start_time.hour + 1
            end_time = time(end_hour if end_hour < 24 else 0, start_time.minute)
            reservation_end = datetime.combine(date, end_time)
            # Handle midnight crossing
            if end_hour >= 24:
                reservation_end = reservation_end + timedelta(days=1)

            time_until_start = reservation_start - berlin_time
            time_until_end = reservation_end - berlin_time

            # Debug logging
            logger.debug(f"Short Notice Check:")
            logger.debug(f"  Reservation start: {reservation_start}")
            logger.debug(f"  Reservation end: {reservation_end}")
            logger.debug(f"  Current time (Berlin): {berlin_time}")
            logger.debug(f"  Time until start: {time_until_start}")
            logger.debug(f"  Time until end: {time_until_end}")

            # If the slot has already ended, it's not short notice (it's invalid/past)
            if time_until_end < timedelta(0):
                logger.debug(f"  Slot has ended, not short notice")
                return False

            # If we're currently within the slot (ongoing), it's short notice
            if time_until_start < timedelta(0) and time_until_end > timedelta(0):
                logger.debug(f"  Currently within the slot (ongoing), IS short notice")
                return True

            # If slot starts within 15 minutes or less, it's short notice
            is_short_notice = time_until_start <= timedelta(minutes=15)
            logger.debug(f"  Within 15 minutes of start: {is_short_notice}")

            return is_short_notice

        except Exception as e:
            logger.error(f"Error in is_short_notice_booking: {e}")
            # Fallback: assume not short notice to be safe
            return False

    @staticmethod
    def classify_booking_type(date, start_time, current_time=None):
        """
        Classify a booking as regular or short notice.

        Args:
            date: Reservation date
            start_time: Reservation start time
            current_time: Current datetime (defaults to now)

        Returns:
            str: 'short_notice' or 'regular'
        """
        if ReservationHelpers.is_short_notice_booking(date, start_time, current_time):
            return 'short_notice'
        return 'regular'
