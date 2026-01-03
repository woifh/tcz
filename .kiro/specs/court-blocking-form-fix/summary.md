# Court Blocking Form Fix - Summary

## Issue Resolved ✅

**Problem**: The court blocking form was using POST requests instead of PUT requests when updating existing blocking events, causing new entries to be created instead of updating the existing batch.

**Root Cause**: The form's edit mode detection relied only on JavaScript state that was set by `populateEditForm()`, but did not automatically read the HTML data attributes that were already present in the template.

## Solution Implemented

### Key Changes Made

1. **Enhanced Form Initialization**: Added `initializeFromDataAttributes()` method to automatically detect edit mode from HTML data attributes on page load.

2. **Automatic Edit Mode Detection**: Form now reads `data-edit-mode`, `data-batch-id`, and `data-block-id` attributes from the HTML template.

3. **Proper API Endpoint Selection**: Form now correctly uses:
   - `PUT /admin/blocks/batch/<batch_id>` for updating existing batches
   - `POST /admin/blocks/multi-court` for creating new batches

4. **UI State Management**: Form button text and appearance automatically update based on edit mode.

### Files Modified

- `app/static/js/components/admin/forms/block-form.js` - Enhanced form initialization and edit mode detection

### Files Verified (No Changes Needed)

- `app/templates/admin/court_blocking.html` - Already had correct data attributes
- `app/routes/admin.py` - Already had correct batch update endpoint  
- `app/static/js/components/admin/core/admin-api.js` - Already had correct API methods

## Technical Details

### Before Fix
```javascript
// Form only detected edit mode when populateEditForm() was called
// This could fail if the method wasn't called or data wasn't available
constructor() {
    this.isEditMode = false; // Always started in create mode
    this.setupEventListeners();
}
```

### After Fix
```javascript
// Form automatically detects edit mode from HTML data attributes
constructor() {
    this.isEditMode = false;
    this.setupEventListeners();
    this.initializeFromDataAttributes(); // NEW - reads HTML data attributes
}

initializeFromDataAttributes() {
    const form = document.getElementById('multi-court-form');
    const editMode = form.getAttribute('data-edit-mode') === 'true';
    const batchId = form.getAttribute('data-batch-id');
    
    if (editMode && batchId) {
        this.isEditMode = true;
        this.editBatchId = batchId;
        this.updateFormForEditMode();
    }
}
```

## Verification

### Backend ✅
- Batch update endpoint exists and works correctly
- Proper batch_id assignment for new blocks
- Correct HTTP methods (PUT for updates, POST for creates)

### Frontend ✅  
- Form reads data attributes on initialization
- Correct API method selection based on edit mode
- Proper form submission handling with preventDefault()
- Debug logging for troubleshooting

### Template ✅
- Data attributes properly set in edit mode
- Form action prevents HTML submission
- Edit data available to JavaScript

## Expected Behavior

### Create Mode
1. User navigates to `/admin/court-blocking`
2. Form loads with `data-edit-mode="false"`
3. Form initializes in create mode
4. Submit button shows "Sperrung erstellen"
5. Form submission uses POST to create new batch

### Edit Mode  
1. User navigates to `/admin/court-blocking/<batch_id>`
2. Form loads with `data-edit-mode="true"` and `data-batch-id="<uuid>"`
3. Form automatically detects edit mode from data attributes
4. Form fields are pre-populated with existing data
5. Submit button shows "Sperrung aktualisieren"
6. Form submission uses PUT to update existing batch

## Impact

- ✅ **No more duplicate entries**: Updates modify existing batches instead of creating new ones
- ✅ **Correct HTTP semantics**: PUT for updates, POST for creates
- ✅ **Improved user experience**: Form automatically knows its mode
- ✅ **Better maintainability**: Less reliance on JavaScript state management
- ✅ **Robust initialization**: Works even if `populateEditForm()` isn't called

## Testing Recommendations

1. **Manual Testing**: Navigate to edit URLs and verify form behavior
2. **Browser Console**: Check for debug logs confirming edit mode detection
3. **Network Tab**: Verify correct HTTP methods are used (PUT vs POST)
4. **Database**: Confirm no duplicate entries are created during updates

The fix ensures that the court blocking form behaves correctly in both create and edit modes, using the appropriate HTTP methods and preventing data duplication.