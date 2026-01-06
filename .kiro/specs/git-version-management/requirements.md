# Requirements Document

## Introduction

The application currently uses a static version number hardcoded in `app/version.py`. This creates manual overhead for version management and makes it difficult to track releases properly. This feature will implement automatic version detection based on Git tags with automatic minor version increments for each commit, providing unique version numbers for every deployment while allowing controlled major releases through tagging.

## Glossary

- **Git_Tag**: A Git reference that points to a specific commit, typically used to mark release points
- **Base_Version**: The version number from the latest Git tag (e.g., "1.2.0")
- **Commit_Count**: The number of commits since the latest version tag
- **Final_Version**: The calculated version combining base version and commit count (e.g., "1.5.0" if base is "1.2.0" and there are 3 commits)
- **Version_System**: The module responsible for determining and providing version information
- **Fallback_Version**: A default version used when no Git tags are available

## Requirements

### Requirement 1: Git Tag Base Version Detection

**User Story:** As a developer, I want the application to use Git tags as the base version, so that I can control major releases through tagging.

#### Acceptance Criteria

1. WHEN the Version_System queries for version information, THE Version_System SHALL read the latest Git tag from the repository as the base version
2. WHEN a valid semantic version tag exists (e.g., "v1.2.3" or "1.2.3"), THE Version_System SHALL use it as the base version
3. WHEN multiple version tags exist, THE Version_System SHALL use the most recent tag based on Git history as the base version
4. WHEN Git tag parsing fails, THE Version_System SHALL log the error and use fallback base version

### Requirement 2: Automatic Minor Version Increment

**User Story:** As a developer, I want the minor version to automatically increment with each commit, so that every deployment has a unique version number.

#### Acceptance Criteria

1. WHEN calculating the final version, THE Version_System SHALL count commits since the latest version tag
2. WHEN commits exist after the latest tag, THE Version_System SHALL increment the minor version by the number of commits
3. WHEN no commits exist after the latest tag, THE Version_System SHALL return the tag version unchanged
4. WHEN counting commits fails, THE Version_System SHALL append the commit hash to indicate the specific build

### Requirement 3: Fallback Version Handling

**User Story:** As a developer, I want the system to gracefully handle cases where Git tags are unavailable, so that the application continues to work in all environments.

#### Acceptance Criteria

1. WHEN no Git tags are found in the repository, THE Version_System SHALL use "0.0.0" as the base version and count all commits
2. WHEN Git commands fail (e.g., not in a Git repository), THE Version_System SHALL return "0.0.0-dev" as the fallback version
3. WHEN Git is not available on the system, THE Version_System SHALL return "0.0.0-dev" as the fallback version
4. WHEN in fallback mode, THE Version_System SHALL include the current commit hash if available

### Requirement 4: Version Format Compatibility

**User Story:** As a system administrator, I want version information to maintain the same format as before, so that existing integrations continue to work.

#### Acceptance Criteria

1. THE Version_System SHALL return version information in the same dictionary format as the current implementation
2. WHEN providing version information, THE Version_System SHALL include the calculated version string in the 'version' field
3. WHEN displaying version information, THE Version_System SHALL show the final calculated version (e.g., "1.5.0" not "1.2.0+3")

### Requirement 5: Git Tag Format Support

**User Story:** As a developer, I want the system to support common Git tag formats, so that I can use standard tagging conventions.

#### Acceptance Criteria

1. WHEN a Git tag starts with "v" (e.g., "v1.2.3"), THE Version_System SHALL strip the "v" prefix and use "1.2.3" as base
2. WHEN a Git tag is a plain version number (e.g., "1.2.3"), THE Version_System SHALL use it as-is as the base version
3. WHEN a Git tag contains additional information (e.g., "v1.2.3-beta"), THE Version_System SHALL use the full tag after stripping the "v" prefix as base
4. WHEN a Git tag doesn't match version patterns, THE Version_System SHALL ignore it and continue searching for valid version tags