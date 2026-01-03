# Implementation Plan: Court Blocking Clone Feature

## Overview

This implementation plan adds "Save as New Event" functionality to the existing court blocking form. The approach extends the current `BlockForm` class and template without requiring new backend endpoints, leveraging the existing multi-court creation API for clone operations.

## Tasks

- [x] 1. Update HTML template for button layout
  - Modify court_blocking.html template to support dynamic button display
  - Add conditional logic for edit mode (3 buttons) vs create mode (1 button)
  - Add "Save as New Event" button with proper styling and positioning
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ]* 1.1 Write property test for button display in edit mode
  - **Property 1: Button display in edit mode**
  - **Validates: Requirements 1.1, 1.3**

- [ ]* 1.2 Write property test for button display in create mode
  - **Property 8: Button display in create mode**
  - **Validates: Requirements 1.2**

- [x] 2. Enhance BlockForm class with clone functionality
  - [x] 2.1 Add clone mode state management
    - Add isCloneMode property and related state variables
    - Implement switchToCloneMode() and resetFromCloneMode() methods
    - Update form state transitions to handle clone mode
    - _Requirements: 3.1, 3.2_

  - [x] 2.2 Implement clone operation handler
    - Add handleCloneSubmit() method for clone button clicks
    - Ensure POST method is used for clone operations (not PUT)
    - Implement proper form data collection for clone operations
    - _Requirements: 2.1, 3.1_

  - [ ]* 2.3 Write property test for clone data preservation
    - **Property 2: Clone operation data preservation**
    - **Validates: Requirements 2.1, 2.6**

  - [ ]* 2.4 Write property test for unique batch ID generation
    - **Property 3: Unique batch ID generation**
    - **Validates: Requirements 2.2, 5.5**

- [ ] 3. Add button state management and validation
  - [ ] 3.1 Implement dynamic button visibility
    - Update updateFormForEditMode() to show/hide appropriate buttons
    - Add logic to display correct buttons based on form mode
    - Ensure proper button positioning and styling
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ] 3.2 Add clone button event listeners
    - Register click handler for "Save as New Event" button
    - Implement button state management during operations
    - Add loading states and disable buttons during async operations
    - _Requirements: 3.3, 4.1_

  - [ ]* 3.3 Write property test for button enablement logic
    - **Property 6: Clone button enablement**
    - **Validates: Requirements 1.5**

- [ ] 4. Implement user feedback and error handling
  - [ ] 4.1 Add loading states and status messages
    - Show loading indicator on clone button during operation
    - Display "Creating new event..." status message
    - Implement proper button state transitions
    - _Requirements: 4.1, 4.2_

  - [ ] 4.2 Add success and error notifications
    - Display success toast notification after successful clone
    - Show error toast with details when clone fails
    - Implement proper error message handling
    - _Requirements: 4.3, 4.4_

  - [ ]* 4.3 Write unit tests for notification display
    - Test success notification after successful clone operations
    - Test error notification after failed clone operations
    - _Requirements: 4.3, 4.4_

- [ ] 5. Add form validation and data integrity
  - [ ] 5.1 Implement clone validation logic
    - Ensure all form fields are validated before clone operation
    - Add court availability checking for clone operations
    - Implement conflict detection and warning display
    - _Requirements: 3.5, 5.1, 5.2_

  - [ ]* 5.2 Write property test for validation consistency
    - **Property 4: Form validation consistency**
    - **Validates: Requirements 3.5, 5.4**

  - [ ]* 5.3 Write property test for court availability validation
    - **Property 7: Court availability validation**
    - **Validates: Requirements 5.1**

  - [ ]* 5.4 Write property test for original event preservation
    - **Property 5: Original event preservation**
    - **Validates: Requirements 3.4**

- [ ] 6. Update form reset and navigation logic
  - [ ] 6.1 Enhance form reset functionality
    - Update resetForm() method to handle clone mode transitions
    - Ensure proper cleanup of clone-related state
    - Implement navigation after successful clone operations
    - _Requirements: 3.2, 2.4_

  - [ ] 6.2 Add conflict resolution handling
    - Implement conflict warning display for overlapping reservations
    - Add override/cancel options for conflict scenarios
    - Ensure proper error handling for conflict situations
    - _Requirements: 5.2, 5.3_

  - [ ]* 6.3 Write unit tests for form state transitions
    - Test form mode transitions (edit → clone → create)
    - Test form reset after successful clone operations
    - Test navigation behavior after clone completion
    - _Requirements: 3.2, 2.4_

- [ ] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Integration testing and final validation
  - [ ] 8.1 Test end-to-end clone workflow
    - Test complete clone operation from edit form to success
    - Verify proper data preservation and unique ID generation
    - Test error scenarios and recovery paths
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [ ]* 8.2 Write integration tests for clone workflow
    - Test complete clone operation with various form data
    - Test error scenarios and proper error handling
    - Test UI feedback during async operations
    - _Requirements: All requirements_

- [ ] 9. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation leverages existing infrastructure to minimize changes
- No new backend endpoints are required - uses existing multi-court creation API