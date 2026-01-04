# Implementation Plan: Sub-reason to Details Refactor

## Overview

This implementation plan covers the systematic refactoring of "sub-reason" terminology to "details" throughout the tennis club reservation system. The approach prioritizes data safety through careful migration, maintains backward compatibility during transition, and ensures comprehensive testing at each step.

## Tasks

- [x] 1. Create database migration for schema changes
  - Create Alembic migration script to rename columns and tables
  - Add data preservation logic to copy existing sub_reason data to details columns
  - Include rollback procedures for safe migration reversal
  - Add foreign key constraint updates for renamed tables
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [ ]* 1.1 Write property test for data preservation during migration
  - **Property 2: Data preservation during migration**
  - **Validates: Requirements 2.5**

- [x] 2. Update database models with new field names
  - Rename sub_reason columns to details in Block, BlockSeries, and BlockTemplate models
  - Rename SubReasonTemplate class to DetailsTemplate
  - Add backward compatibility properties for sub_reason access
  - Update model relationships and backref names
  - _Requirements: 4.1, 4.6_

- [ ]* 2.1 Write unit tests for model field access
  - Test that details field stores and retrieves values correctly
  - Test backward compatibility properties work as expected
  - _Requirements: 4.1, 4.6_

- [x] 3. Update service layer method signatures and implementations
  - Update BlockService method parameters from sub_reason to details
  - Update method implementations to use details field names
  - Add parameter mapping for backward compatibility where needed
  - Update template management methods for DetailsTemplate
  - _Requirements: 4.2, 4.5_

- [ ]* 3.1 Write property test for programmatic block creation
  - **Property 6: Programmatic block creation consistency**
  - **Validates: Requirements 4.5**

- [x] 4. Update API routes and handlers
  - Update route handlers to accept details parameter instead of sub_reason
  - Update API response formatting to return details field
  - Update template management endpoints from sub-reason-templates to details-templates
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.3_

- [ ]* 4.1 Write property test for API backward compatibility
  - **Property 4: Backward compatibility mapping**
  - **Validates: Requirements 3.6**

- [ ]* 4.2 Write property test for API response consistency
  - **Property 3: API response field consistency**
  - **Validates: Requirements 3.3**

- [x] 5. Checkpoint - Ensure backend changes work correctly
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Update HTML templates and form elements
  - Replace "Sub-reason" labels with "Details" in all admin templates
  - Update form input names from sub_reason to details
  - Update German text from "Zusätzlicher Grund" to "Details"
  - Update template management UI to show "Details Templates"
  - _Requirements: 1.1, 1.3, 6.1, 6.2, 6.4_

- [ ]* 6.1 Write unit tests for UI terminology
  - Test that rendered templates contain "Details" labels
  - Test that templates do not contain "Sub-reason" text
  - _Requirements: 1.1, 1.3_

- [x] 7. Update JavaScript code and frontend logic
  - Update variable names from subReason to details in all JS files
  - Update DOM element IDs and selectors to use details naming
  - Update API call parameters to use details instead of sub_reason
  - Update admin constants and localization strings
  - _Requirements: 1.2, 1.4, 1.5_

- [ ]* 7.1 Write property test for UI terminology consistency
  - **Property 1: UI terminology consistency**
  - **Validates: Requirements 1.2**

- [x] 8. Update database query usage throughout codebase
  - Update all database queries to reference details column instead of sub_reason
  - Update filter operations to use details field name
  - Update audit log generation to reference details in operation descriptions
  - _Requirements: 4.4, 1.5_

- [ ]* 8.1 Write property test for database query field usage
  - **Property 5: Database query field usage**
  - **Validates: Requirements 4.4**

- [x] 9. Update test files and scripts
  - Update all test scripts to use details instead of sub_reason in test data
  - Update property-based tests to validate details field behavior
  - Update integration tests to use details API parameters
  - Update end-to-end tests to check for Details labels in UI
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 9.1 Write integration tests for refactored functionality
  - Test complete workflows use new details terminology
  - Test backward compatibility works in integration scenarios
  - _Requirements: 5.4_

- [x] 10. Update German localization and error messages
  - Update German interface text to use "Details" consistently
  - Update German help text to reference Details instead of Untergrund
  - Update German error messages to reference Details in validation
  - Update German template management to show Details-Vorlagen
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ]* 10.1 Write unit tests for German localization
  - Test German interface displays correct terminology
  - Test German error messages use Details terminology
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 11. Run database migration and verify data integrity
  - Execute the migration script on development database
  - Verify all existing data is preserved and accessible
  - Test that all foreign key relationships still work
  - Verify indexes are recreated correctly
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [ ]* 11.1 Write comprehensive migration validation tests
  - Test migration preserves all data correctly
  - Test rollback procedures work if needed
  - _Requirements: 2.5, 2.6_

- [ ] 12. Final integration testing and validation
  - Run complete test suite to ensure no regressions
  - Test all admin workflows use new Details terminology
  - Test that UI consistently shows Details instead of Sub-reason
  - _Requirements: All requirements_

- [ ] 13. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster implementation
- Each task references specific requirements for traceability
- Migration task (Task 1) should be executed carefully with proper backups
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The refactoring maintains all existing functionality while improving terminology