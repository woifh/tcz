"""JSON serialization utilities."""
from datetime import datetime, date, time


def serialize_for_json(value):
    """
    Convert date/time objects (including nested structures) to JSON-safe strings.

    Args:
        value: Any value that may contain datetime objects

    Returns:
        JSON-serializable version of the value with datetimes converted to ISO format
    """
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: serialize_for_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize_for_json(v) for v in value]
    return value
