"""
Reservation service - Backward compatibility shim.

This module has been refactored into a package structure for better organization.
The original 672-line file has been split into focused sub-services:

- app/services/reservation/helpers.py (ReservationHelpers)
- app/services/reservation/query_service.py (ReservationQueryService)
- app/services/reservation/creation_service.py (ReservationCreationService)
- app/services/reservation/cancellation_service.py (ReservationCancellationService)

This file now serves as a backward compatibility layer, re-exporting the
unified ReservationService class from the package.

All existing code that imports from this module will continue to work without
any changes.
"""

# Import the unified service from the new package
from app.services.reservation import (
    ReservationService,
    ReservationHelpers,
    ReservationQueryService,
    ReservationCreationService,
    ReservationCancellationService
)

# Export for backward compatibility
__all__ = [
    'ReservationService',
    'ReservationHelpers',
    'ReservationQueryService',
    'ReservationCreationService',
    'ReservationCancellationService'
]
