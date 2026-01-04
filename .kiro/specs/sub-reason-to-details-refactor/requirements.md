# Requirements Document

## Introduction

This specification covers the refactoring of the "sub-reason" terminology to "details" throughout the tennis club reservation system. The current system uses "sub_reason" in database fields, API parameters, and user interfaces to provide additional context for court blocking events. This refactoring will make the terminology more user-friendly and intuitive while maintaining all existing functionality.

## Glossary

- **Block**: An administrative restriction preventing court bookings for specified time periods
- **Block Reason**: A customizable category explaining why a court is blocked (e.g., Maintenance, Championship, Tennis Course)
- **Block Details**: Additional specific information about a block (formerly called "sub-reason")
- **Details Template**: A predefined template for common block details (formerly called "sub-reason template")
- **Database Migration**: A script that safely updates database schema and data
- **API Endpoint**: A URL route that handles HTTP requests for specific functionality

## Requirements

### Requirement 1

**User Story:** As a system administrator, I want the blocking interface to use "Details" instead of "Sub-reason", so that the terminology is more intuitive and user-friendly.

#### Acceptance Criteria

1. WHEN an administrator views the block creation form, THE System SHALL display "Details" as the field label instead of "Sub-reason"
2. WHEN an administrator views existing blocks, THE System SHALL show "Details" in column headers and display text instead of "Sub-reason"
3. WHEN an administrator manages templates, THE System SHALL display "Details Templates" instead of "Sub-reason Templates"
4. WHEN an administrator filters blocks, THE System SHALL show "Details" in filter options instead of "Sub-reason"
5. WHEN an administrator views block audit logs, THE System SHALL display "Details" in operation descriptions instead of "Sub-reason"

### Requirement 2

**User Story:** As a developer, I want the database schema to use "details" field names, so that the code is consistent with the user-facing terminology.

#### Acceptance Criteria

1. WHEN the database migration runs, THE System SHALL rename the "sub_reason" column to "details" in the block table
2. WHEN the database migration runs, THE System SHALL rename the "sub_reason" column to "details" in the block_series table
3. WHEN the database migration runs, THE System SHALL rename the "sub_reason" column to "details" in the block_template table
4. WHEN the database migration runs, THE System SHALL rename the "sub_reason_template" table to "details_template"
5. WHEN the migration completes, THE System SHALL preserve all existing data without loss
6. WHEN the migration completes, THE System SHALL maintain all foreign key relationships and indexes

### Requirement 3

**User Story:** As a developer, I want the API endpoints to use "details" parameters, so that the API is consistent with the updated terminology.

#### Acceptance Criteria

1. WHEN creating a block via API, THE System SHALL accept "details" parameter instead of "sub_reason"
2. WHEN updating a block via API, THE System SHALL accept "details" parameter instead of "sub_reason"
3. WHEN retrieving blocks via API, THE System SHALL return "details" field instead of "sub_reason"
4. WHEN filtering blocks via API, THE System SHALL accept "details" filter parameter instead of "sub_reason"
5. WHEN managing details templates via API, THE System SHALL use "details_templates" endpoints instead of "sub_reason_templates"
6. WHEN the API receives legacy "sub_reason" parameters, THE System SHALL maintain backward compatibility by mapping them to "details"

### Requirement 4

**User Story:** As a developer, I want the Python code to use "details" variable names and method parameters, so that the codebase is consistent and maintainable.

#### Acceptance Criteria

1. WHEN defining model properties, THE System SHALL use "details" instead of "sub_reason"
2. WHEN defining service method parameters, THE System SHALL use "details" instead of "sub_reason"
3. WHEN defining route handler parameters, THE System SHALL use "details" instead of "sub_reason"
4. WHEN accessing database fields in queries, THE System SHALL use "details" column name
5. WHEN creating new blocks programmatically, THE System SHALL use "details" parameter name
6. WHEN the code references template models, THE System SHALL use "DetailsTemplate" class name instead of "SubReasonTemplate"

### Requirement 5

**User Story:** As a system administrator, I want existing test data and scripts to continue working, so that the refactoring doesn't break development and testing workflows.

#### Acceptance Criteria

1. WHEN running existing test scripts, THE System SHALL update them to use "details" instead of "sub_reason"
2. WHEN creating test data, THE System SHALL use "details" field names in database operations
3. WHEN running property-based tests, THE System SHALL validate "details" field behavior instead of "sub_reason"
4. WHEN running integration tests, THE System SHALL verify "details" API parameters work correctly
5. WHEN running end-to-end tests, THE System SHALL confirm "Details" labels appear in the UI

### Requirement 6

**User Story:** As a system user, I want the German translations to reflect the new terminology, so that the interface remains properly localized.

#### Acceptance Criteria

1. WHEN viewing the German interface, THE System SHALL display "Details" as "Details" (keeping English term as it's commonly used)
2. WHEN viewing German help text, THE System SHALL use "Details" instead of "Untergrund" for consistency
3. WHEN viewing German error messages, THE System SHALL reference "Details" in validation messages
4. WHEN viewing German template management, THE System SHALL show "Details-Vorlagen" instead of "Untergrund-Vorlagen"