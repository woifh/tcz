# Court Blocking Form Fix - Requirements

## Problem Statement

The court blocking form is currently using POST requests instead of PUT requests when updating existing blocking events. This causes new entries to be created instead of updating the existing batch.

## Current Issues

1. **Form submission method**: The form is submitting via HTML form submission instead of using JavaScript API calls
2. **Edit mode detection**: The form is not properly detecting edit mode from HTML data attributes
3. **Batch ID handling**: The form is not using the batch_id for updates

## Root Cause Analysis

1. The form has proper `preventDefault()` and event listeners set up
2. The backend has the correct batch update endpoint (`PUT /admin/blocks/batch/<batch_id>`)
3. The frontend API has the correct `updateBatch()` method
4. However, the form's edit mode detection relies only on JavaScript state, not HTML data attributes
5. When the page loads with edit data, the form should automatically be in edit mode

## User Stories

### US-1: Form Edit Mode Detection
**As an** admin user  
**I want** the court blocking form to automatically detect edit mode from the page data  
**So that** updates use PUT requests instead of creating new entries

**Acceptance Criteria:**
- Form reads `data-edit-mode`, `data-batch-id` attributes on initialization
- Form automatically sets edit mode when these attributes are present
- Form uses batch_id for updates instead of individual block IDs

### US-2: Proper API Method Selection
**As an** admin user  
**I want** the form to use the correct HTTP method based on the operation  
**So that** updates modify existing entries and creates make new entries

**Acceptance Criteria:**
- Edit mode uses PUT request to `/admin/blocks/batch/<batch_id>`
- Create mode uses POST request to `/admin/blocks/multi-court`
- Form prevents HTML form submission and uses JavaScript API calls

### US-3: Edit Data Population
**As an** admin user  
**I want** the form to be pre-populated with existing data when editing  
**So that** I can see current values and make changes

**Acceptance Criteria:**
- Form fields are populated with existing block data
- Court checkboxes are pre-selected based on batch data
- Form button text changes to "Aktualisieren" in edit mode

## Technical Requirements

### Frontend Changes
1. Modify `BlockForm` constructor to read HTML data attributes
2. Add initialization method to set edit mode from data attributes
3. Ensure `populateEditForm()` is called when edit data is available
4. Verify form submission uses correct API endpoints

### Backend Verification
1. Confirm batch update endpoint works correctly
2. Verify batch_id is properly passed in edit URLs
3. Ensure edit template renders correct data attributes

## Success Criteria

1. ✅ Edit form uses PUT requests to update existing batches
2. ✅ Create form uses POST requests to create new batches  
3. ✅ Form automatically detects edit mode from page data
4. ✅ No new entries are created when updating existing blocks
5. ✅ Form validation works in both create and edit modes

## Testing Scenarios

### Test Case 1: Edit Existing Batch
1. Navigate to edit URL for existing batch
2. Modify form fields (courts, time, reason)
3. Submit form
4. Verify PUT request is sent to batch endpoint
5. Verify existing batch is updated, not duplicated

### Test Case 2: Create New Batch
1. Navigate to court blocking page (no edit data)
2. Fill out form fields
3. Submit form
4. Verify POST request is sent to multi-court endpoint
5. Verify new batch is created

### Test Case 3: Form State Management
1. Load edit page
2. Verify form is in edit mode automatically
3. Verify form fields are pre-populated
4. Verify button text shows "Aktualisieren"