# Design Document

## Overview

The "Save as New Event" feature extends the existing court blocking form to support cloning operations. This design leverages the current form infrastructure while adding new UI elements and state management to handle clone operations alongside existing create and update functionality.

## Architecture

The feature integrates with the existing court blocking system architecture:

- **Frontend**: Enhanced `BlockForm` class with clone operation support
- **Backend**: Utilizes existing `/admin/blocks/multi-court` POST endpoint for clone operations
- **State Management**: Extended form state to distinguish between edit, create, and clone modes
- **UI Components**: Additional button and enhanced form controls

## Components and Interfaces

### Frontend Components

#### Enhanced BlockForm Class
```javascript
class BlockForm {
    // Existing properties
    isEditMode: boolean
    editBlockId: string
    editBatchId: string
    
    // New properties for clone support
    isCloneMode: boolean
    originalBatchId: string
    
    // New methods
    handleCloneSubmit(event): Promise<void>
    switchToCloneMode(): void
    resetFromCloneMode(): void
    updateButtonStates(): void
}
```

#### Button Component Structure
```html
<!-- Edit Mode: 3 buttons -->
<div class="form-actions">
    <button id="update-block-btn" type="submit">Update Event</button>
    <button id="clone-block-btn" type="button">Save as New Event</button>
    <button id="cancel-btn" type="button">Cancel</button>
</div>

<!-- Create Mode: 1 button -->
<div class="form-actions">
    <button id="create-block-btn" type="submit">Create Event</button>
</div>
```

### Backend Integration

#### Existing Endpoint Usage
- **Clone Operation**: Uses existing `POST /admin/blocks/multi-court` endpoint
- **Update Operation**: Uses existing `PUT /admin/blocks/batch/{batch_id}` endpoint
- **No new backend endpoints required**

#### Data Flow
```
Clone Button Click → Form Validation → POST to multi-court endpoint → 
Success Response → Toast Notification → Page Refresh/Redirect
```

## Data Models

### Form State Model
```javascript
{
    mode: 'create' | 'edit' | 'clone',
    isEditMode: boolean,
    isCloneMode: boolean,
    editBlockId: string | null,
    editBatchId: string | null,
    originalBatchId: string | null, // Preserved for reference
    formData: {
        court_ids: number[],
        date: string,
        start_time: string,
        end_time: string,
        reason_id: number,
        sub_reason: string
    }
}
```

### Clone Operation Payload
```javascript
{
    court_ids: number[],
    date: string,
    start_time: string,
    end_time: string,
    reason_id: number,
    sub_reason: string
    // Note: No batch_id - new one will be generated
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

<function_calls>
<invoke name="prework">
<parameter name="featureName">court-blocking-clone-feature

### Property Reflection

After reviewing the prework analysis, I identified several redundant properties that can be consolidated:

- Properties 2.2 and 5.5 both test unique batch_id generation - can be combined
- Properties 2.1 and 2.6 both test data preservation - can be combined into comprehensive data preservation property
- Properties 3.4 and data integrity testing can be combined
- Properties 5.1 and 5.4 both test validation consistency - can be combined

### Converting EARS to Properties

Property 1: Button display in edit mode
*For any* form in edit mode, the form should display exactly three buttons with labels "Update", "Save as New Event", and "Cancel" in that order
**Validates: Requirements 1.1, 1.3**

Property 8: Button display in create mode
*For any* form in create mode, the form should display exactly one button with label "Create Event"
**Validates: Requirements 1.2**

Property 2: Clone operation data preservation
*For any* valid form data, cloning an event should create a new event with identical court selections, date, times, reason, and sub-reason
**Validates: Requirements 2.1, 2.6**

Property 3: Unique batch ID generation
*For any* clone operation, the new event should have a batch_id that is different from the original event's batch_id
**Validates: Requirements 2.2, 5.5**

Property 4: Form validation consistency
*For any* form data that fails validation for create operations, the same data should fail validation for clone operations
**Validates: Requirements 3.5, 5.4**

Property 5: Original event preservation
*For any* clone operation, the original blocking event should remain completely unchanged after the clone completes
**Validates: Requirements 3.4**

Property 6: Clone button enablement
*For any* form state, the "Save as New Event" button should be enabled if and only if all required fields are valid
**Validates: Requirements 1.5**

Property 7: Court availability validation
*For any* clone operation with court/time combinations, the system should validate court availability and reject conflicts consistently
**Validates: Requirements 5.1**

## Error Handling

### Clone Operation Errors
- **Validation Errors**: Display field-specific error messages, keep form in edit mode
- **Network Errors**: Display generic error toast, retry option available
- **Server Errors**: Display server error message, log for debugging
- **Conflict Errors**: Display conflict details with override options

### Form State Errors
- **Invalid State Transitions**: Reset to known good state (edit mode)
- **Missing Data**: Reload form data from server
- **Concurrent Modifications**: Warn user and offer refresh option

## Testing Strategy

### Unit Tests
- Button visibility and positioning in different form modes (edit: 3 buttons, create: 1 button)
- Form state transitions (edit → clone → create)
- Event handler registration and cleanup
- Form validation with various input combinations
- Error message display and clearing

### Property-Based Tests
Each property test should run minimum 100 iterations and be tagged with the format:
**Feature: court-blocking-clone-feature, Property {number}: {property_text}**

1. **Property 1**: Generate random form states in edit mode, verify button display (3 buttons)
2. **Property 2**: Generate random valid form data, clone and verify data preservation
3. **Property 3**: Generate random events, clone and verify unique batch_ids
4. **Property 4**: Generate random invalid form data, verify consistent validation
5. **Property 5**: Generate random events, clone and verify original unchanged
6. **Property 6**: Generate random form states, verify button enablement logic
7. **Property 7**: Generate random court/time combinations, verify availability validation
8. **Property 8**: Generate random form states in create mode, verify button display (1 button)

### Integration Tests
- End-to-end clone workflow from edit form to success
- Clone operation with various form data combinations
- Error scenarios and recovery paths
- UI feedback during async operations
- Navigation after successful clone operations

### Manual Testing Scenarios
- Visual distinction between buttons (styling verification)
- Loading states and animations
- Toast notification appearance and timing
- Form responsiveness during operations
- Accessibility compliance for new UI elements