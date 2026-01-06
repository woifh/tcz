"""Query helper utilities for common database query patterns."""

from datetime import date, time
from sqlalchemy import or_, and_


def build_active_reservation_time_filter(current_date: date, current_time: time, reservation_model):
    """
    Build a time-based filter for active reservations.

    A reservation is considered active if it hasn't ended yet, meaning:
    - It's on a future date, OR
    - It's today but the end time hasn't passed yet

    Args:
        current_date: Current date in Berlin timezone
        current_time: Current time in Berlin timezone (time only, no date)
        reservation_model: The Reservation model class (to access its columns)

    Returns:
        SQLAlchemy filter expression for active reservations

    Example:
        >>> from app.models import Reservation
        >>> from datetime import date, time
        >>> current_date = date(2024, 1, 15)
        >>> current_time = time(14, 30)
        >>> time_filter = build_active_reservation_time_filter(current_date, current_time, Reservation)
        >>> query = Reservation.query.filter(time_filter)
    """
    return or_(
        reservation_model.date > current_date,  # Future date
        and_(
            reservation_model.date == current_date,  # Same date
            reservation_model.end_time > current_time  # But hasn't ended yet
        )
    )


def build_active_block_time_filter(current_date: date, current_time: time, block_model):
    """
    Build a time-based filter for active blocks.

    A block is considered active if it hasn't ended yet, meaning:
    - It's on a future date, OR
    - It's today but the end time hasn't passed yet

    Args:
        current_date: Current date in Berlin timezone
        current_time: Current time in Berlin timezone (time only, no date)
        block_model: The Block model class (to access its columns)

    Returns:
        SQLAlchemy filter expression for active blocks

    Example:
        >>> from app.models import Block
        >>> from datetime import date, time
        >>> current_date = date(2024, 1, 15)
        >>> current_time = time(14, 30)
        >>> time_filter = build_active_block_time_filter(current_date, current_time, Block)
        >>> query = Block.query.filter(time_filter)
    """
    return or_(
        block_model.date > current_date,  # Future date
        and_(
            block_model.date == current_date,  # Same date
            block_model.end_time > current_time  # But hasn't ended yet
        )
    )
