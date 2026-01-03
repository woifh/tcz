# Implementation Plan: Reservation Time Update

## Overview

Update the tennis club reservation system to change operating hours from 6am-10pm to 8am-10pm. This involves configuration changes, frontend updates, and validation adjustments while preserving historical data.

## Tasks

- [x] 1. Update core configuration
  - Update BOOKING_START_HOUR from 6 to 8 in config.py
  - Verify configuration is loaded correctly across application
  - _Requirements: 4.1, 4.2_

- [x] 2. Update court availability service
  - [x] 2.1 Modify time slot generation in courts.py
    - Change range(6, 22) to range(8, 22) in get_availability function
    - Update comment to reflect new time range (08:00 to 21:00) with 14 slots
    - _Requirements: 1.1, 1.3_

  - [ ]* 2.2 Write property test for time slot generation
    - **Property 1: Time slot generation consistency**
    - **Validates: Requirements 1.1, 1.3**

- [x] 3. Update admin panel form defaults
  - [x] 3.1 Update HTML template defaults
    - Change default value from "06:00" to "08:00" in admin.html
    - Change default value from "06:00" to "08:00" in court_blocking.html
    - Change default end time from "22:00" to "21:00" (last bookable slot starts at 21:00)
    - _Requirements: 3.1, 3.2, 3.3_

  - [x] 3.2 Update JavaScript form module defaults
    - Update default time in block-form.js
    - Update default time in series-form.js  
    - Update default time in template-form.js
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 3.3 Write property test for form defaults
    - **Property 3: Form default consistency**
    - **Validates: Requirements 3.1, 3.2, 3.3**

- [x] 4. Update validation and error handling
  - [x] 4.1 Update validation service (if exists)
    - Modify time range validation to accept 08:00-21:00
    - Update error messages to reflect new hours
    - _Requirements: 1.4, 2.4_

  - [x] 4.2 Update validation error messages
    - Change error message to "Buchungen sind nur zwischen 08:00 und 21:00 Uhr möglich"
    - _Requirements: 1.4_

  - [ ]* 4.3 Write property test for validation boundaries
    - **Property 4: Validation boundary enforcement**
    - **Validates: Requirements 1.4, 2.4**

- [x] 5. Checkpoint - Test configuration changes
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Update frontend components
  - [x] 6.1 Verify dashboard displays correct time range
    - Test that availability grid shows 08:00-21:00 slots
    - Verify booking modal respects new time limits
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ]* 6.2 Write integration tests for frontend
    - Test dashboard time slot display
    - Test booking modal time restrictions
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 7. Verify historical data preservation
  - [x] 7.1 Test existing reservations display
    - Ensure reservations outside new hours are still visible
    - Verify no data loss for historical bookings
    - _Requirements: 2.4, 4.3_

  - [ ]* 7.2 Write property test for data preservation
    - **Property 5: Historical data preservation**
    - **Validates: Requirements 2.4, 4.3**

- [x] 8. Final testing and verification
  - [x] 8.1 Run comprehensive test suite
    - Execute all unit tests
    - Execute all property-based tests
    - Execute all integration tests
    - _Requirements: All_

  - [x] 8.2 Manual testing verification
    - Test dashboard shows correct time range (08:00-21:00)
    - Test booking forms reject invalid times
    - Test admin forms default to 08:00
    - Verify existing data is preserved
    - _Requirements: All_

- [x] 9. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster implementation
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Historical data preservation is critical - no existing reservations should be lost