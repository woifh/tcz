# Implementation Plan: Teamster Role Management

## Overview

This implementation plan adds a "teamster" role to the Tennis Club Reservation System, providing intermediate permissions between regular members and administrators. The implementation follows a layered approach: model extensions, authorization decorators, service modifications, route creation, and UI customization.

## Tasks

- [x] 1. Extend Member model with teamster role methods
  - Add `is_teamster()`, `can_manage_blocks()`, and `can_edit_block()` methods to Member class
  - Ensure backward compatibility with existing role system
  - _Requirements: 1.1, 1.3, 8.1_

- [ ]* 1.1 Write property test for role system integrity
  - **Property 1: Role System Integrity**
  - **Validates: Requirements 1.1, 1.3**

- [ ]* 1.2 Write property test for role assignment consistency
  - **Property 2: Role Assignment Consistency**
  - **Validates: Requirements 1.2, 1.4**

- [x] 2. Create teamster authorization decorators
  - Add `teamster_required` and `block_owner_or_admin_required` decorators to auth.py
  - Implement proper error handling for JSON and HTML responses
  - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [ ]* 2.1 Write property test for authentication uniformity
  - **Property 3: Authentication Uniformity**
  - **Validates: Requirements 2.1**

- [ ]* 2.2 Write property test for authorization hierarchy
  - **Property 4: Authorization Hierarchy**
  - **Validates: Requirements 2.3, 2.4, 2.5, 8.1, 8.2, 8.3**

- [x] 3. Enhance BlockService with ownership methods
  - Add `get_blocks_for_user()` and `can_user_delete_batch()` methods
  - Implement ownership filtering and metadata for UI
  - _Requirements: 4.1, 4.4_

- [ ]* 3.1 Write property test for block creation ownership
  - **Property 5: Block Creation Ownership**
  - **Validates: Requirements 3.1, 4.3**

- [ ]* 3.2 Write property test for batch block consistency
  - **Property 6: Batch Block Consistency**
  - **Validates: Requirements 3.2**

- [ ]* 3.3 Write property test for conflict resolution parity
  - **Property 7: Conflict Resolution Parity**
  - **Validates: Requirements 3.3**

- [x] 4. Create teamster route blueprint
  - Create `app/routes/teamster/` directory with `__init__.py`, `views.py`, and `blocks.py`
  - Implement teamster-specific routes for block management
  - Register teamster blueprint in main application
  - _Requirements: 6.1, 6.5_

- [ ]* 4.1 Write property test for ownership-based edit permissions
  - **Property 8: Ownership-Based Edit Permissions**
  - **Validates: Requirements 4.1, 4.2**

- [ ]* 4.2 Write property test for batch deletion ownership
  - **Property 9: Batch Deletion Ownership**
  - **Validates: Requirements 4.4**

- [x] 5. Implement teamster block management routes
  - Create POST route for block creation with teamster permissions
  - Create PUT route for block editing with ownership checks
  - Create DELETE route for batch deletion with ownership validation
  - _Requirements: 3.1, 3.2, 4.3, 4.4_

- [ ]* 5.1 Write property test for block reason access consistency
  - **Property 10: Block Reason Access Consistency**
  - **Validates: Requirements 5.1, 5.3**

- [ ] 6. Create teamster UI templates
  - Create `app/templates/teamster/` directory with base template and blocks template
  - Implement role-based UI elements and ownership indicators
  - _Requirements: 6.3, 6.4_

- [ ]* 6.1 Write property test for UI element visibility
  - **Property 11: UI Element Visibility**
  - **Validates: Requirements 6.1, 6.2, 6.4**

- [ ] 7. Modify existing admin routes for teamster compatibility
  - Update admin block routes to work with teamster permissions
  - Add role-based filtering to block listing endpoints
  - _Requirements: 4.1, 6.1_

- [ ]* 7.1 Write property test for audit trail completeness
  - **Property 12: Audit Trail Completeness**
  - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

- [ ] 8. Enhance audit logging for role tracking
  - Add role information to BlockAuditLog display
  - Modify audit log queries to include role context
  - _Requirements: 7.4, 7.5_

- [ ]* 8.1 Write property test for permission inheritance consistency
  - **Property 13: Permission Inheritance Consistency**
  - **Validates: Requirements 8.2, 8.3**

- [ ] 9. Update navigation and access control
  - Modify main navigation to show appropriate links for teamsters
  - Hide block reason management from teamster interface
  - Add access control to prevent teamster access to restricted admin functions
  - _Requirements: 5.2, 6.2_

- [ ]* 9.1 Write property test for real-time permission updates
  - **Property 14: Real-time Permission Updates**
  - **Validates: Requirements 8.4**

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Integration testing and final validation
  - Test complete teamster workflow: login → create blocks → edit own blocks → delete own blocks
  - Test admin override capabilities
  - Verify audit trail completeness
  - _Requirements: All requirements validation_

- [ ]* 11.1 Write integration tests for teamster workflow
  - Test end-to-end teamster functionality
  - Test admin override scenarios
  - Test mixed admin/teamster audit trails

- [ ] 12. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties across all inputs
- Integration tests validate complete user workflows
- The implementation maintains backward compatibility with existing member and administrator roles
- All teamster operations are logged in the audit trail for administrative oversight