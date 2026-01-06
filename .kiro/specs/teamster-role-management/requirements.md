# Requirements Document

## Introduction

This feature introduces a new user role called "teamster" (Mannschaftsführer) to the Tennis Club Reservation System. The teamster role provides an intermediate permission level between regular members and administrators, specifically focused on court blocking capabilities for team management purposes.

## Glossary

- **System**: The Tennis Club Reservation System
- **Teamster**: A member with elevated permissions for team management (Mannschaftsführer)
- **Member**: A regular club member with basic reservation privileges
- **Administrator**: A user with full system privileges
- **Block**: A court availability restriction that prevents reservations
- **Block_Reason**: A predefined reason category for court blocks
- **Batch_Block**: A group of blocks created together, identified by a shared batch_id

## Requirements

### Requirement 1: Teamster Role Creation

**User Story:** As a system administrator, I want to assign teamster roles to specific members, so that they can manage court blocks for their teams without full administrative privileges.

#### Acceptance Criteria

1. THE System SHALL support a new role type "teamster" in addition to existing "member" and "administrator" roles
2. WHEN an administrator assigns the teamster role to a member, THE System SHALL update the member's role field to "teamster"
3. THE System SHALL maintain backward compatibility with existing member and administrator roles
4. WHEN a member's role is changed to teamster, THE System SHALL preserve all existing member data and relationships

### Requirement 2: Teamster Authentication and Authorization

**User Story:** As a teamster, I want to access court blocking functionality, so that I can manage court availability for my team activities.

#### Acceptance Criteria

1. WHEN a teamster logs in, THE System SHALL authenticate them with the same login process as other users
2. THE System SHALL provide teamster-specific authorization decorators for route protection
3. WHEN a teamster accesses a teamster-protected route, THE System SHALL grant access
4. WHEN a regular member accesses a teamster-protected route, THE System SHALL deny access with appropriate error message
5. WHEN an administrator accesses a teamster-protected route, THE System SHALL grant access (admin inherits teamster permissions)

### Requirement 3: Teamster Block Creation Permissions

**User Story:** As a teamster, I want to create court blocks, so that I can reserve courts for team training and matches.

#### Acceptance Criteria

1. WHEN a teamster creates a single court block, THE System SHALL create the block with the teamster as the creator
2. WHEN a teamster creates multiple court blocks simultaneously, THE System SHALL create all blocks with a shared batch_id
3. WHEN a teamster creates a block, THE System SHALL cancel conflicting reservations following the same rules as administrator blocks
4. WHEN a teamster creates a block, THE System SHALL log the operation in the audit trail

### Requirement 4: Teamster Block Management Restrictions

**User Story:** As a teamster, I want to manage only my own blocks, so that I maintain responsibility for my team's court usage while respecting other teamsters' blocks.

#### Acceptance Criteria

1. WHEN a teamster views blocks, THE System SHALL display all blocks but only allow editing of blocks they created
2. WHEN a teamster can't edit a block created by another user as THE System SHALL not show an edit button
3. WHEN a teamster edits their own block, THE System SHALL update the block
4. WHEN a teamster deletes their own block batch, THE System SHALL remove all blocks in that batch

### Requirement 5: Block Reason Access Restrictions

**User Story:** As a system administrator, I want teamsters to use existing block reasons but not manage them, so that reason categories remain consistent across the system.

#### Acceptance Criteria

1. WHEN a teamster creates a block, THE System SHALL provide access to all active block reasons
2. THe system will not show the bock reason management menu to teamsters
3. WHEN a teamster accesses block reason management routes, THE System SHALL deny access with appropriate error message

### Requirement 6: User Interface Access Control

**User Story:** As a teamster, I want to access appropriate administrative interfaces for my permitted functions, so that I can efficiently manage my team's court blocks.

#### Acceptance Criteria

1. WHEN a teamster accesses the admin interface, THE System SHALL display only block management functionality
2. THE System SHALL hide member management, system settings, and other administrative functions from teamsters
3. WHEN a teamster views the block management interface, THE System SHALL clearly indicate which blocks they can edit
4. THE System SHALL provide visual indicators by not providing edit buttons for blocks the teamster cannot modify
5. WHEN a teamster creates blocks, THE System SHALL use the same interface workflow as administrators

### Requirement 7: Audit Trail and Accountability

**User Story:** As a system administrator, I want to track all teamster actions, so that I can maintain oversight of court block management.

#### Acceptance Criteria

1. WHEN a teamster creates a block, THE System SHALL log the action in the BlockAuditLog with the teamster's ID
2. WHEN a teamster modifies a block, THE System SHALL log the modification with details of what changed
3. WHEN a teamster deletes blocks, THE System SHALL log the deletion with the affected block details
4. THE System SHALL distinguish between administrator and teamster actions in audit logs
5. WHEN administrators view audit logs, THE System SHALL display the role of the user who performed each action

### Requirement 8: Permission Inheritance and Hierarchy

**User Story:** As a system architect, I want clear permission hierarchy, so that the system maintains security while providing appropriate access levels.

#### Acceptance Criteria

1. THE System SHALL maintain the permission hierarchy: Administrator > Teamster > Member
2. WHEN checking permissions, THE System SHALL grant administrator access to all teamster-protected resources
3. THE System SHALL deny member access to teamster-protected resources
4. WHEN a user's role changes, THE System SHALL immediately apply the new permission level
5. THE System SHALL maintain existing administrator permissions without modification