# Requirements Document

## Introduction

This feature adds the ability to clone existing court blocking events, allowing administrators to quickly create new events based on existing ones with modified parameters. This enhances the user experience by reducing repetitive data entry when creating similar blocking events.

## Glossary

- **Admin**: A user with administrative privileges who can manage court blocking events
- **Blocking_Event**: A court reservation block that prevents regular bookings during specified times
- **Clone_Operation**: The process of creating a new blocking event based on an existing one
- **Edit_Form**: The form interface used to modify existing blocking events
- **Batch_ID**: Unique identifier for a group of related blocking events across multiple courts

## Requirements

### Requirement 1: Clone Button Display

**User Story:** As an admin, I want to see a "Save as New Event" button when editing existing blocking events, so that I can easily create similar events without starting from scratch.

#### Acceptance Criteria

1. WHEN an admin accesses the edit form for an existing blocking event, THE System SHALL display three action buttons: "Update", "Save as New Event", and "Cancel"
2. WHEN the form is in create mode (new event), THE System SHALL only display a "Create Event" button
3. WHEN the "Save as New Event" button is displayed, THE System SHALL position it between the "Update" and "Cancel" buttons
4. THE "Save as New Event" button SHALL be visually distinct from the primary "Update" button
5. THE "Save as New Event" button SHALL be enabled when all required form fields are valid

### Requirement 2: Clone Operation Execution

**User Story:** As an admin, I want to click "Save as New Event" to create a duplicate blocking event, so that I can quickly create similar events with minor modifications.

#### Acceptance Criteria

1. WHEN an admin clicks "Save as New Event", THE System SHALL create a new blocking event with the current form data
2. WHEN creating the cloned event, THE System SHALL generate a new unique batch_id for the new event
3. WHEN the clone operation succeeds, THE System SHALL display a success message indicating the new event was created
4. WHEN the clone operation succeeds, THE System SHALL redirect to the main court blocking page or refresh the events list
5. WHEN the clone operation fails, THE System SHALL display an error message and remain on the edit form
6. THE cloned event SHALL preserve all form data including court selections, date, times, reason, and sub-reason

### Requirement 3: Form State Management

**User Story:** As an admin, I want the form to handle clone operations correctly, so that the system maintains proper state and doesn't interfere with normal edit operations.

#### Acceptance Criteria

1. WHEN a clone operation is initiated, THE System SHALL use POST method to create the new event (not PUT)
2. WHEN a clone operation completes successfully, THE System SHALL reset the form state to create mode
3. WHEN a clone operation is in progress, THE System SHALL disable all action buttons to prevent duplicate submissions
4. THE original blocking event SHALL remain unchanged after a clone operation
5. THE System SHALL validate all form fields before allowing clone operation to proceed

### Requirement 4: User Interface Feedback

**User Story:** As an admin, I want clear feedback during clone operations, so that I understand what's happening and can respond appropriately to success or failure.

#### Acceptance Criteria

1. WHEN an admin clicks "Save as New Event", THE System SHALL show a loading indicator on the button
2. WHEN the clone operation is in progress, THE System SHALL display "Creating new event..." or similar status message
3. WHEN the clone operation succeeds, THE System SHALL display a toast notification with success message
4. WHEN the clone operation fails, THE System SHALL display a toast notification with error details
5. THE System SHALL provide clear visual feedback to distinguish clone operations from update operations

### Requirement 5: Data Integrity and Validation

**User Story:** As an admin, I want cloned events to maintain data integrity, so that the new events are valid and don't conflict with existing reservations.

#### Acceptance Criteria

1. WHEN creating a cloned event, THE System SHALL validate that the selected courts are available for the specified time
2. WHEN court conflicts exist, THE System SHALL display conflict warnings before proceeding with clone operation
3. WHEN a cloned event would overlap with existing reservations, THE System SHALL provide options to override or cancel
4. THE cloned event SHALL have all the same validation rules as manually created events
5. THE System SHALL ensure the cloned event has a unique batch_id different from the original event