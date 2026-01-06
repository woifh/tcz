"""Timezone handling decorators for service methods."""

import logging
from functools import wraps
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def with_berlin_timezone(param_name: str = 'current_time', log_operation: bool = True):
    """
    Decorator that automatically handles Berlin timezone conversion for service methods.

    This decorator:
    1. Takes a datetime parameter from the method arguments
    2. Converts it to Berlin timezone
    3. Extracts date and time components
    4. Passes them to the wrapped function as additional parameters
    5. Optionally logs the timezone operation

    Args:
        param_name: Name of the datetime parameter to convert (default: 'current_time')
        log_operation: Whether to log the timezone operation (default: True)

    The decorator adds these parameters to the wrapped function:
        - berlin_time: The full datetime in Berlin timezone
        - berlin_date: Just the date component
        - berlin_time_only: Just the time component

    Example:
        @with_berlin_timezone()
        def get_active_reservations(self, current_time=None, berlin_time=None,
                                    berlin_date=None, berlin_time_only=None):
            # berlin_time, berlin_date, berlin_time_only are automatically populated
            query = Reservation.query.filter(Reservation.date >= berlin_date)
            ...

    Usage in service methods:
        # Before:
        berlin_time = ensure_berlin_timezone(current_time)
        log_timezone_operation("method_name", current_time, berlin_time)
        current_date = berlin_time.date()
        current_time_only = berlin_time.time()

        # After:
        @with_berlin_timezone()
        def method_name(self, current_time=None, berlin_date=None, berlin_time_only=None):
            # berlin_date and berlin_time_only are automatically available
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Import here to avoid circular imports
                from app.utils.timezone_utils import ensure_berlin_timezone, log_timezone_operation

                # Get the datetime parameter from kwargs
                current_time = kwargs.get(param_name)

                # If not in kwargs, try to get from args based on function signature
                if current_time is None:
                    import inspect
                    sig = inspect.signature(func)
                    param_names = list(sig.parameters.keys())

                    # Try to find the parameter in args
                    if param_name in param_names:
                        param_index = param_names.index(param_name)
                        # Adjust for 'self' parameter in methods
                        if param_index < len(args):
                            current_time = args[param_index]

                # Convert to Berlin timezone
                berlin_time = ensure_berlin_timezone(current_time)

                # Log the operation if requested
                if log_operation:
                    log_timezone_operation(func.__name__, current_time, berlin_time)

                # Extract date and time components
                berlin_date = berlin_time.date()
                berlin_time_only = berlin_time.time()

                # Add the new parameters to kwargs
                kwargs['berlin_time'] = berlin_time
                kwargs['berlin_date'] = berlin_date
                kwargs['berlin_time_only'] = berlin_time_only

                # Call the original function
                return func(*args, **kwargs)

            except Exception as e:
                logger.error(f"Error in with_berlin_timezone decorator for {func.__name__}: {e}")
                # Re-raise to let the function's own error handling deal with it
                raise

        return wrapper
    return decorator


def with_berlin_timezone_simple(func):
    """
    Simplified version of with_berlin_timezone that always uses 'current_time' parameter.

    This is a convenience decorator that doesn't require any arguments.

    Example:
        @with_berlin_timezone_simple
        def get_active_reservations(self, current_time=None, berlin_date=None,
                                    berlin_time_only=None):
            # berlin_date and berlin_time_only are automatically populated
            ...
    """
    return with_berlin_timezone()(func)
