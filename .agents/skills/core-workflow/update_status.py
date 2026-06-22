#!/usr/bin/env python3
"""
update_status.py

Update the progress journal markdown file.
Used by the executor to track execution state after each phase.

Usage:
  python update_status.py <progress_file> <phase> <status> [details]
  
Status values: COMPLETE, FAILED, IN_PROGRESS, ROLLED_BACK

Example:
  python update_status.py auth_caching_PROGRESS.md 1 COMPLETE "Created cache.py"
"""

import sys
import os
import re
from datetime import datetime, timezone


def update_progress_file(progress_file, phase, status, details=""):
    """Update the progress journal with the new status."""
    
    # Read existing file or create new one
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Create new progress file with template
        content = f"""# Execution Progress Journal

**Plan**: {{feature}}_{{phase}}_implementation_plan.md
**Started**: {datetime.now(timezone.utc).isoformat()}
**Last Updated**: {datetime.now(timezone.utc).isoformat()}
**Executing Agent**: Unknown

## Overall Status
- [ ] Phase 1 — TBD

## Current Phase
**Phase**: 1
**Status**: IN_PROGRESS

## Last Completed Action
Initializing...

## Next Action Required
Begin phase execution.

## Files Modified This Session
(none yet)

## Failures & Decisions
(none yet)
"""
    
    # Update Last Updated timestamp
    content = re.sub(
        r"\*\*Last Updated\*\*:\s*[^\n]+",
        f"**Last Updated**: {datetime.now(timezone.utc).isoformat()}",
        content
    )
    
    # Update Current Phase status
    content = re.sub(
        r"(\*\*Status\*\*:)\s*[A-Z_]+",
        f"\\1 {status}",
        content,
        count=1
    )
    
    # Update Last Completed Action
    if details:
        content = re.sub(
            r"## Last Completed Action\n[^\n]*",
            f"## Last Completed Action\n{details}",
            content
        )
    
    # Write updated content
    with open(progress_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Progress updated: {progress_file}")
    print(f"   Phase: {phase}, Status: {status}")
    if details:
        print(f"   Details: {details}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python update_status.py <progress_file> <phase> <status> [details]", file=sys.stderr)
        print("Status: COMPLETE, FAILED, IN_PROGRESS, ROLLED_BACK", file=sys.stderr)
        sys.exit(1)
    
    progress_file = sys.argv[1]
    phase = sys.argv[2]
    status = sys.argv[3]
    details = sys.argv[4] if len(sys.argv) > 4 else ""
    
    # Validate status
    valid_statuses = ['COMPLETE', 'FAILED', 'IN_PROGRESS', 'ROLLED_BACK']
    if status not in valid_statuses:
        print(f"Error: Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}", file=sys.stderr)
        sys.exit(1)
    
    update_progress_file(progress_file, phase, status, details)


if __name__ == "__main__":
    main()
