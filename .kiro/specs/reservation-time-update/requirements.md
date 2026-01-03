# Requirements Document

## Introduction

This specification covers updating the court reservation system to change the operating hours from the current 6am-10pm schedule to a new 8am-10pm schedule. This change affects the available booking time slots for all court reservations.

## Glossary

- **System**: The tennis club reservation web application
- **Booking_Slot**: A one-hour time period during which a court can be reserved
- **Operating_Hours**: The time range during which court reservations are allowed
- **Time_Slot**: A specific hour-long period (e.g., 08:00-09:00)

## Requirements

### Requirement 1

**User Story:** As a club administrator, I want to update the reservation system operating hours from 6am-10pm to 8am-10pm, so that the booking schedule aligns with the club's new operating policy.

#### Acceptance Criteria

1. THE System SHALL allow reservations only for time slots between 08:00 and 21:00
2. THE System SHALL define booking slots at hourly intervals: 08:00-09:00, 09:00-10:00, through 21:00-22:00
3. WHEN the availability grid is displayed, THE System SHALL show time slots starting from 08:00 and ending at 21:00
4. WHEN a member attempts to book outside the new operating hours (before 08:00 or after 21:00), THE System SHALL reject the booking with an appropriate error message

### Requirement 2

**User Story:** As a club member, I want the booking interface to reflect the new operating hours, so that I can only see and select available time slots within the 8am-10pm range.

#### Acceptance Criteria

1. WHEN viewing the court availability dashboard, THE System SHALL display a grid with rows representing hours from 08:00 to 21:00
2. WHEN using the booking modal, THE System SHALL only allow selection of time slots between 08:00 and 21:00
3. THE System SHALL update all time slot dropdowns and selectors to reflect the new 08:00-21:00 range
4. WHEN displaying existing reservations, THE System SHALL continue to show all historical bookings regardless of their time slots

### Requirement 3

**User Story:** As a system administrator, I want the admin panel blocking functionality to use the new time range defaults, so that block creation forms are pre-populated with appropriate times.

#### Acceptance Criteria

1. WHEN creating new court blocks in the admin panel, THE System SHALL default the start time to 08:00 instead of 06:00
2. WHEN creating recurring block series, THE System SHALL default the start time to 08:00 instead of 06:00
3. WHEN creating block templates, THE System SHALL default the start time to 08:00 instead of 06:00
4. THE System SHALL continue to allow admin users to create blocks outside the standard operating hours if needed for maintenance or special events

### Requirement 4

**User Story:** As a developer, I want the time range configuration to be centralized and consistent, so that future changes can be made easily without affecting system reliability.

#### Acceptance Criteria

1. THE System SHALL use a single configuration source for defining booking start and end hours
2. WHEN the booking hours configuration is changed, THE System SHALL apply the change consistently across all components (dashboard, booking forms, validation, admin panels)
3. THE System SHALL maintain backward compatibility with existing reservations that may fall outside the new operating hours
4. THE System SHALL update validation rules to reflect the new 08:00-21:00 time range