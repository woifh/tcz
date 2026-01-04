# Design Document

## Overview

This design covers the comprehensive refactoring of "sub-reason" terminology to "details" throughout the tennis club reservation system. The refactoring involves database schema changes, API parameter updates, frontend interface modifications, and code variable renaming while maintaining backward compatibility and data integrity.

## Architecture

The refactoring follows a systematic approach across all system layers:

1. **Database Layer**: Schema migration to rename columns and tables
2. **Model Layer**: Update Python model classes and properties
3. **Service Layer**: Update method parameters and variable names
4. **API Layer**: Update route handlers and response formats with backward compatibility
5. **Frontend Layer**: Update JavaScript code and HTML templates
6. **Localization Layer**: Update German translations

## Components and Interfaces

### Database Schema Changes

**Current Schema:**
```sql
-- Block table
CREATE TABLE block (
    id INT PRIMARY KEY,
    court_id INT,
    date DATE,
    start_time TIME,
    end_time TIME,
    reason_id INT,
    sub_reason VARCHAR(255),  -- TO BE RENAMED
    series_id INT,
    batch_id VARCHAR(36),
    is_modified BOOLEAN,
    created_by_id INT,
    created_at TIMESTAMP
);

-- BlockSeries table
CREATE TABLE block_series (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    start_time TIME,
    end_time TIME,
    recurrence_pattern VARCHAR(20),
    recurrence_days JSON,
    reason_id INT,
    sub_reason VARCHAR(255),  -- TO BE RENAMED
    created_by_id INT,
    created_at TIMESTAMP
);

-- BlockTemplate table
CREATE TABLE block_template (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    court_selection JSON,
    start_time TIME,
    end_time TIME,
    reason_id INT,
    sub_reason VARCHAR(255),  -- TO BE RENAMED
    recurrence_pattern VARCHAR(20),
    recurrence_days JSON,
    created_by_id INT,
    created_at TIMESTAMP
);

-- SubReasonTemplate table
CREATE TABLE sub_reason_template (  -- TO BE RENAMED
    id INT PRIMARY KEY,
    reason_id INT,
    template_name VARCHAR(100),
    created_by_id INT,
    created_at TIMESTAMP
);
```

**New Schema:**
```sql
-- Block table
CREATE TABLE block (
    id INT PRIMARY KEY,
    court_id INT,
    date DATE,
    start_time TIME,
    end_time TIME,
    reason_id INT,
    details VARCHAR(255),  -- RENAMED FROM sub_reason
    series_id INT,
    batch_id VARCHAR(36),
    is_modified BOOLEAN,
    created_by_id INT,
    created_at TIMESTAMP
);

-- BlockSeries table
CREATE TABLE block_series (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    start_time TIME,
    end_time TIME,
    recurrence_pattern VARCHAR(20),
    recurrence_days JSON,
    reason_id INT,
    details VARCHAR(255),  -- RENAMED FROM sub_reason
    created_by_id INT,
    created_at TIMESTAMP
);

-- BlockTemplate table
CREATE TABLE block_template (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    court_selection JSON,
    start_time TIME,
    end_time TIME,
    reason_id INT,
    details VARCHAR(255),  -- RENAMED FROM sub_reason
    recurrence_pattern VARCHAR(20),
    recurrence_days JSON,
    created_by_id INT,
    created_at TIMESTAMP
);

-- DetailsTemplate table
CREATE TABLE details_template (  -- RENAMED FROM sub_reason_template
    id INT PRIMARY KEY,
    reason_id INT,
    template_name VARCHAR(100),
    created_by_id INT,
    created_at TIMESTAMP
);
```

### Model Layer Updates

**Current Models:**
```python
class Block(db.Model):
    sub_reason = db.Column(db.String(255), nullable=True)

class BlockSeries(db.Model):
    sub_reason = db.Column(db.String(255), nullable=True)

class BlockTemplate(db.Model):
    sub_reason = db.Column(db.String(255), nullable=True)

class SubReasonTemplate(db.Model):
    __tablename__ = 'sub_reason_template'
```

**New Models:**
```python
class Block(db.Model):
    details = db.Column(db.String(255), nullable=True)
    
    # Backward compatibility property
    @property
    def sub_reason(self):
        return self.details
    
    @sub_reason.setter
    def sub_reason(self, value):
        self.details = value

class BlockSeries(db.Model):
    details = db.Column(db.String(255), nullable=True)
    
    # Backward compatibility property
    @property
    def sub_reason(self):
        return self.details
    
    @sub_reason.setter
    def sub_reason(self, value):
        self.details = value

class BlockTemplate(db.Model):
    details = db.Column(db.String(255), nullable=True)
    
    # Backward compatibility property
    @property
    def sub_reason(self):
        return self.details
    
    @sub_reason.setter
    def sub_reason(self, value):
        self.details = value

class DetailsTemplate(db.Model):  # RENAMED FROM SubReasonTemplate
    __tablename__ = 'details_template'
    
    # Relationships updated
    reason = db.relationship('BlockReason', backref='details_templates')
```

### Service Layer Updates

**Current Service Methods:**
```python
class BlockService:
    @staticmethod
    def create_block(court_id, date, start_time, end_time, reason_id, sub_reason, admin_id):
        pass
    
    @staticmethod
    def create_multi_court_blocks(court_ids, date, start_time, end_time, reason_id, sub_reason, admin_id):
        pass
    
    @staticmethod
    def create_recurring_block_series(court_ids, start_date, end_date, start_time, end_time, 
                                    recurrence_pattern, recurrence_days, reason_id, sub_reason, 
                                    admin_id, series_name):
        pass
```

**New Service Methods:**
```python
class BlockService:
    @staticmethod
    def create_block(court_id, date, start_time, end_time, reason_id, details, admin_id):
        # Support both parameter names for backward compatibility
        pass
    
    @staticmethod
    def create_multi_court_blocks(court_ids, date, start_time, end_time, reason_id, details, admin_id):
        pass
    
    @staticmethod
    def create_recurring_block_series(court_ids, start_date, end_date, start_time, end_time, 
                                    recurrence_pattern, recurrence_days, reason_id, details, 
                                    admin_id, series_name):
        pass
    
    # New methods for details template management
    @staticmethod
    def create_details_template(reason_id, template_name, admin_id):
        pass
    
    @staticmethod
    def get_details_templates(reason_id):
        pass
    
    @staticmethod
    def delete_details_template(template_id, admin_id):
        pass
```

### API Layer Updates

**Current API Endpoints:**
```
POST /admin/blocks
- Parameters: sub_reason

PUT /admin/blocks/<id>
- Parameters: sub_reason

GET /admin/blocks
- Response: sub_reason field

GET /admin/block-reasons/<id>/sub-reason-templates
POST /admin/block-reasons/<id>/sub-reason-templates
DELETE /admin/sub-reason-templates/<id>
```

**New API Endpoints:**
```
POST /admin/blocks
- Parameters: details (accepts both details and sub_reason for backward compatibility)

PUT /admin/blocks/<id>
- Parameters: details (accepts both details and sub_reason for backward compatibility)

GET /admin/blocks
- Response: details field (includes sub_reason for backward compatibility)

GET /admin/block-reasons/<id>/details-templates
POST /admin/block-reasons/<id>/details-templates
DELETE /admin/details-templates/<id>

# Legacy endpoints maintained for backward compatibility
GET /admin/block-reasons/<id>/sub-reason-templates (redirects to details-templates)
POST /admin/block-reasons/<id>/sub-reason-templates (redirects to details-templates)
DELETE /admin/sub-reason-templates/<id> (redirects to details-templates)
```

### Frontend Layer Updates

**HTML Template Changes:**
```html
<!-- Current -->
<label>Zusätzlicher Grund (optional)</label>
<input type="text" id="multi-sub-reason" name="sub_reason">

<!-- New -->
<label>Details (optional)</label>
<input type="text" id="multi-details" name="details">
```

**JavaScript Variable Updates:**
```javascript
// Current
const subReasonInput = document.getElementById('bulk-edit-sub-reason');
editData.sub_reason = formData.sub_reason;

// New
const detailsInput = document.getElementById('bulk-edit-details');
editData.details = formData.details;
```

## Data Models

### Migration Strategy

**Migration Steps:**
1. Create new columns with "details" names
2. Copy data from old columns to new columns
3. Update foreign key references for table renames
4. Drop old columns and tables
5. Update indexes and constraints

**Data Preservation:**
- All existing sub_reason data will be copied to details columns
- No data loss during migration
- Foreign key relationships maintained
- Indexes recreated with new column names

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

Based on the prework analysis, the following properties ensure the refactoring maintains system correctness:

### Property 1: UI terminology consistency
*For any* admin interface page that displays block information, all field labels and headers should use "Details" terminology and not contain "Sub-reason" text
**Validates: Requirements 1.2**

### Property 2: Data preservation during migration
*For any* existing block record before migration, the details field after migration should contain exactly the same value that was in the sub_reason field before migration
**Validates: Requirements 2.5**

### Property 3: API response field consistency
*For any* API response that includes block data, the response should contain a "details" field and should not contain a "sub_reason" field in the primary response structure
**Validates: Requirements 3.3**

### Property 4: Backward compatibility mapping
*For any* API request that includes legacy "sub_reason" parameters, the system should accept the request and map the parameter value to the "details" field internally
**Validates: Requirements 3.6**

### Property 5: Database query field usage
*For any* database query that accesses block detail information, the query should reference the "details" column name and not the "sub_reason" column name
**Validates: Requirements 4.4**

### Property 6: Programmatic block creation consistency
*For any* programmatic block creation operation, the system should accept and properly store values passed to the "details" parameter
**Validates: Requirements 4.5**

## Error Handling

### Migration Error Handling
- **Data Loss Prevention**: Migration includes rollback procedures if any step fails
- **Constraint Validation**: All foreign key relationships are validated before and after migration
- **Backup Requirements**: Full database backup required before migration execution

### API Backward Compatibility
- **Parameter Mapping**: Legacy "sub_reason" parameters are automatically mapped to "details"
- **Response Format**: Responses include both "details" and "sub_reason" fields during transition period
- **Error Messages**: Clear error messages when deprecated endpoints are used

### Frontend Graceful Degradation
- **Progressive Enhancement**: New "Details" terminology is applied progressively
- **Fallback Handling**: System continues to function if some UI elements still show old terminology
- **User Feedback**: Clear indication when legacy features are being phased out

## Testing Strategy

### Dual Testing Approach
The refactoring requires both unit tests and property-based tests to ensure comprehensive coverage:

**Unit Tests:**
- Verify specific migration steps complete successfully
- Test individual API endpoint parameter acceptance
- Validate specific UI elements display correct terminology
- Check database schema changes are applied correctly

**Property-Based Tests:**
- Verify data preservation across all existing records during migration
- Test API backward compatibility across all possible parameter combinations
- Validate UI terminology consistency across all admin interfaces
- Ensure database queries use correct field names across all operations

**Property Test Configuration:**
- Minimum 100 iterations per property test
- Each property test references its design document property
- Tag format: **Feature: sub-reason-to-details-refactor, Property {number}: {property_text}**

### Migration Testing Strategy
- **Pre-migration validation**: Verify current data integrity
- **Migration simulation**: Test migration on copy of production data
- **Post-migration validation**: Verify all data preserved and accessible
- **Rollback testing**: Verify rollback procedures work correctly

### Integration Testing Strategy
- **API compatibility testing**: Test both new and legacy parameter names
- **Frontend integration**: Verify UI updates work with backend changes
- **End-to-end workflows**: Test complete admin workflows use new terminology
- **Cross-browser compatibility**: Ensure UI changes work across browsers
