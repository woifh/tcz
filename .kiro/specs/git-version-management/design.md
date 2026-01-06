# Design Document: Git Version Management

## Overview

This design implements automatic version management based on Git tags with commit-based minor version increments. The system will replace the static `VERSION = "1.0.0"` constant with dynamic version calculation that uses Git tags as base versions and increments the minor version for each commit since the last tag.

The design maintains full backward compatibility with the existing version API while providing automatic, unique version numbers for every deployment.

## Architecture

The version management system follows a layered approach:

```
┌─────────────────────────────────────┐
│           Version API               │
│      (get_version_info)             │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│        Version Calculator           │
│   (calculate_version_from_git)      │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│         Git Operations              │
│  (get_latest_tag, count_commits)    │
└─────────────────────────────────────┘
```

## Components and Interfaces

### Git Operations Layer

**Purpose**: Handle all Git command execution and parsing
**Location**: `app/version.py`

```python
def get_latest_version_tag() -> Optional[str]:
    """Get the most recent version tag from Git history."""
    
def count_commits_since_tag(tag: str) -> int:
    """Count commits since the specified tag."""
    
def parse_version_tag(tag: str) -> str:
    """Parse and normalize a version tag (strip 'v' prefix, etc.)."""
```

### Version Calculator

**Purpose**: Calculate final version from Git information
**Location**: `app/version.py`

```python
def calculate_version_from_git() -> str:
    """Calculate version using Git tags and commit count."""
    
def increment_minor_version(base_version: str, increment: int) -> str:
    """Increment the minor version by the specified amount."""
```

### Version API (Modified)

**Purpose**: Provide version information to the application
**Location**: `app/version.py`

```python
def get_version_info() -> dict:
    """Get complete version information (maintains existing interface)."""
```

## Data Models

### Version Information Structure

The existing version info dictionary structure is maintained:

```python
{
    'version': str,           # Calculated version (e.g., "1.5.0")
    'commit_hash': str,       # Current commit hash
    'branch': str,            # Current branch name
    'last_commit_date': str,  # Last commit timestamp
    'deployment_time': str    # Current deployment time
}
```

### Version Calculation Logic

```
Base Version (from tag): "1.2.0"
Commits Since Tag: 3
Final Version: "1.5.0"

Calculation:
- Parse base: major=1, minor=2, patch=0
- Add commits to minor: minor = 2 + 3 = 5
- Result: "1.5.0"
```

## Implementation Details

### Git Tag Discovery

The system will use `git describe --tags --abbrev=0` to find the latest tag, then filter for version-like tags:

```python
def get_latest_version_tag() -> Optional[str]:
    try:
        # Get all tags sorted by version
        result = subprocess.check_output([
            'git', 'tag', '--sort=-version:refname'
        ], stderr=subprocess.DEVNULL, cwd=repo_root)
        
        tags = result.decode('utf-8').strip().split('\n')
        
        # Find first tag that looks like a version
        for tag in tags:
            if re.match(r'^v?\d+\.\d+\.\d+', tag):
                return tag
                
        return None
    except:
        return None
```

### Commit Counting

Count commits between the latest tag and HEAD:

```python
def count_commits_since_tag(tag: str) -> int:
    try:
        result = subprocess.check_output([
            'git', 'rev-list', '--count', f'{tag}..HEAD'
        ], stderr=subprocess.DEVNULL, cwd=repo_root)
        
        return int(result.decode('utf-8').strip())
    except:
        return 0
```

### Version Calculation

```python
def calculate_version_from_git() -> str:
    # Get base version from latest tag
    latest_tag = get_latest_version_tag()
    
    if latest_tag:
        base_version = parse_version_tag(latest_tag)
        commit_count = count_commits_since_tag(latest_tag)
        
        if commit_count > 0:
            return increment_minor_version(base_version, commit_count)
        else:
            return base_version
    else:
        # No tags found - count all commits from initial commit
        total_commits = count_total_commits()
        return f"0.{total_commits}.0"
```

### Error Handling Strategy

1. **Git Command Failures**: Return fallback version "0.0.0-dev"
2. **Invalid Tag Formats**: Skip and continue searching
3. **No Repository**: Return fallback version with warning log
4. **Parsing Errors**: Log error and use fallback

## Migration Strategy

### Phase 1: Replace Static Version
- Remove `VERSION = "1.0.0"` constant
- Implement `calculate_version_from_git()` function
- Update `get_version_info()` to use calculated version
- Maintain exact same API interface

### Phase 2: Add Logging and Error Handling
- Add comprehensive error handling
- Add debug logging for version calculation
- Add fallback mechanisms

### Phase 3: Testing and Validation
- Test with various Git tag scenarios
- Test fallback behavior
- Validate version endpoint compatibility

## Testing Strategy

The testing approach combines unit tests for specific scenarios and property-based tests for comprehensive coverage.

### Unit Tests
- Test specific Git tag formats ("v1.2.3", "1.2.3", "1.2.3-beta")
- Test commit counting scenarios
- Test fallback behavior when Git is unavailable
- Test version calculation edge cases

### Property-Based Tests
Property-based tests will validate universal behaviors across many generated inputs using the Hypothesis library with minimum 100 iterations per test.

Each property test will be tagged with: **Feature: git-version-management, Property {number}: {property_text}**

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Tag Selection and Parsing
*For any* Git repository with version tags, the system should correctly identify the most recent valid version tag and parse it into a clean base version (stripping "v" prefixes and handling various formats consistently).
**Validates: Requirements 1.1, 1.2, 1.3, 5.1, 5.2, 5.3**

### Property 2: Version Calculation Consistency
*For any* base version and commit count, incrementing the minor version by the commit count should produce a valid semantic version where the minor version equals the original minor version plus the commit count.
**Validates: Requirements 2.1, 2.2**

### Property 3: API Format Consistency
*For any* version calculation result, the returned version information should maintain the expected dictionary structure with all required fields present and the calculated version in the 'version' field.
**Validates: Requirements 4.1, 4.2, 4.4**

### Property 4: Error Handling Graceful Degradation
*For any* Git operation failure scenario, the system should return a valid fallback version without crashing and include available information when possible.
**Validates: Requirements 1.4, 2.4, 3.4**

### Property 5: Tag Filtering
*For any* repository containing both valid and invalid tags, the system should ignore non-version tags and only consider tags that match semantic version patterns.
**Validates: Requirements 5.4**

## Error Handling

### Git Command Failures
- **Scenario**: Git commands fail due to missing Git, corrupted repository, or permission issues
- **Response**: Log the specific error and return fallback version "0.0.0-dev"
- **Recovery**: Include commit hash if available through alternative means

### Invalid Tag Formats
- **Scenario**: Repository contains tags that don't match version patterns
- **Response**: Skip invalid tags and continue searching for valid ones
- **Fallback**: If no valid tags found, treat as untagged repository

### Version Calculation Errors
- **Scenario**: Arithmetic errors in version increment or parsing failures
- **Response**: Log error details and return base version with commit hash appended
- **Example**: "1.2.0-abc123f" instead of calculated version

### Repository State Issues
- **Scenario**: Detached HEAD, shallow clone, or missing commit history
- **Response**: Use available information and clearly indicate limitations in logs
- **Graceful**: Always return a valid version string, never crash

## Testing Strategy

### Unit Tests
Unit tests will verify specific examples and edge cases:
- Specific tag formats ("v1.2.3", "1.2.3-beta", "2.0.0")
- Error conditions (no Git, corrupted repo, invalid tags)
- Edge cases (no commits after tag, no tags in repo)
- API compatibility (exact dictionary structure)

### Property-Based Tests
Property-based tests will verify universal properties using Hypothesis library with minimum 100 iterations per test. Each test will be tagged with: **Feature: git-version-management, Property {number}: {property_text}**

**Test Configuration:**
- Library: Hypothesis (Python property-based testing)
- Iterations: Minimum 100 per property test
- Generators: Custom generators for Git repositories, version tags, and commit histories
- Shrinking: Enabled to find minimal failing examples

**Generator Strategy:**
- **Version Tags**: Generate semantic versions with various prefixes and suffixes
- **Commit Histories**: Generate realistic commit counts and repository states
- **Error Conditions**: Generate various failure scenarios systematically
- **Repository States**: Generate different Git repository configurations

The dual testing approach ensures both concrete examples work correctly (unit tests) and universal properties hold across all possible inputs (property tests).