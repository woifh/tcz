# Design Document

## Overview

This design covers the implementation of updated reservation operating hours, changing from 6am-10pm to 8am-10pm. The change involves updating configuration values, modifying time slot generation logic, updating default values in forms, and ensuring validation rules reflect the new time range.

## Architecture

The time range change affects multiple layers of the application:

1. **Configuration Layer**: Central configuration in `config.py`
2. **Service Layer**: Time slot generation and validation logic
3. **API Layer**: Court availability endpoints and validation
4. **Frontend Layer**: Form defaults and time slot displays
5. **Admin Layer**: Block creation form defaults

## Components and Interfaces

### Configuration Component
- **File**: `config.py`
- **Change**: Update `BOOKING_START_HOUR` from 6 to 8
- **Impact**: All components that reference this configuration

### Court Availability Service
- **File**: `app/routes/courts.py`
- **Function**: `get_availability()`
- **Change**: Update time slot generation loop from `range(6, 22)` to `range(8, 22)`
- **Impact**: Reduces available time slots from 16 to 14 slots per day

### Admin Panel Forms
- **Files**: 
  - `app/templates/admin.html`
  - `app/templates/admin/court_blocking.html`
  - `app/static/js/components/admin/forms/block-form.js`
  - `app/static/js/components/admin/forms/series-form.js`
  - `app/static/js/components/admin/forms/template-form.js`
- **Change**: Update default time values from "06:00" to "08:00"

### Validation Service
- **File**: `app/services/validation_service.py` (if exists)
- **Change**: Update time range validation to accept 08:00-21:00 range
- **Impact**: Booking attempts outside new hours will be rejected

## Data Models

No database schema changes are required. The existing reservation and block models will continue to work with the new time range. Historical data with times outside the new range will be preserved.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Time slot generation consistency
*For any* date request to the availability endpoint, the generated time slots should start at 08:00 and end at 21:00 with exactly 14 one-hour slots.
**Validates: Requirements 1.1, 1.3**

### Property 2: Configuration consistency
*For any* component that uses booking hours, the start hour should be 8 and end hour should be 22 (last slot 21:00-22:00).
**Validates: Requirements 4.1, 4.2**

### Property 3: Form default consistency
*For any* admin form that has time inputs, the default start time should be "08:00" instead of "06:00".
**Validates: Requirements 3.1, 3.2, 3.3**

### Property 4: Validation boundary enforcement
*For any* booking attempt with start time before 08:00 or after 21:00, the system should reject the booking with appropriate error message.
**Validates: Requirements 1.4, 2.4**

### Property 5: Historical data preservation
*For any* existing reservation or block with times outside the new 08:00-21:00 range, the data should remain accessible and unchanged.
**Validates: Requirements 2.4, 4.3**

## Error Handling

### Invalid Time Range Errors
- **Scenario**: User attempts to book before 08:00 or after 21:00
- **Response**: HTTP 400 with German error message "Buchungen sind nur zwischen 08:00 und 21:00 Uhr möglich"
- **Frontend**: Display error toast notification

### Configuration Validation
- **Scenario**: Invalid configuration values
- **Response**: Application startup validation to ensure BOOKING_START_HOUR = 8
- **Fallback**: Log error and use default values

## Testing Strategy

### Unit Tests
- Test time slot generation with new range (8-22)
- Test form default values are "08:00"
- Test validation rejects times outside 08:00-21:00
- Test configuration loading and validation

### Property-Based Tests
- **Property 1 Test**: Generate random dates and verify all returned time slots are within 08:00-21:00 range
- **Property 2 Test**: Verify all components use consistent configuration values
- **Property 4 Test**: Generate random invalid times (before 08:00, after 21:00) and verify all are rejected

### Integration Tests
- Test dashboard displays correct time range
- Test booking modal only allows valid times
- Test admin forms have correct defaults
- Test existing reservations outside new range are still displayed

### Manual Testing
- Verify dashboard shows 08:00-21:00 time slots
- Verify booking forms reject invalid times
- Verify admin panel forms default to 08:00
- Verify existing historical data is preserved

## Implementation Plan

### Phase 1: Configuration Update
1. Update `BOOKING_START_HOUR` in `config.py`
2. Update time slot generation in `courts.py`
3. Test availability endpoint returns correct range

### Phase 2: Frontend Updates
1. Update default values in HTML templates
2. Update default values in JavaScript form modules
3. Test form defaults are correct

### Phase 3: Validation Updates
1. Update validation error messages
2. Update any hardcoded time range checks
3. Test validation rejects invalid times

### Phase 4: Testing and Verification
1. Run all automated tests
2. Manual testing of all affected components
3. Verify historical data preservation
4. Performance testing with new time range