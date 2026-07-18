#!/usr/bin/env bash
# Smoke tests for core-workflow and qa-workflow plugins.
# Validates structural integrity — SKILL.md frontmatter, plugin.json refs, no hardcoded paths.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(dirname "$(dirname "$PLUGIN_DIR")")"
FAIL=0

pass() { echo "  ✅ $1"; }
fail() { echo "  ❌ $1"; FAIL=1; }

echo "=== Core-Workflow Smoke Tests ==="

# 1. Every SKILL.md has name and description in frontmatter
echo ""
echo "--- Checking SKILL.md frontmatter ---"
for skill in "$PLUGIN_DIR"/skills/*/SKILL.md; do
  name=$(basename "$(dirname "$skill")")
  if head -20 "$skill" | grep -q '^name:'; then
    pass "$name: has 'name' field"
  else
    fail "$name: missing 'name' field in frontmatter"
  fi
  if head -20 "$skill" | grep -q '^description:'; then
    pass "$name: has 'description' field"
  else
    fail "$name: missing 'description' field in frontmatter"
  fi
done

# 2. plugin.json is valid JSON and references existing files
echo ""
echo "--- Checking plugin.json ---"
if python3 -c "import json; json.load(open('$PLUGIN_DIR/plugin.json'))" 2>/dev/null; then
  pass "plugin.json is valid JSON"
else
  fail "plugin.json is not valid JSON"
fi

# Check skill references exist
for skill_path in $(python3 -c "
import json
with open('$PLUGIN_DIR/plugin.json') as f:
    d = json.load(f)
for v in d.get('skills', {}).values():
    print(v)
" 2>/dev/null); do
  if [ -f "$PLUGIN_DIR/$skill_path" ]; then
    pass "plugin.json ref exists: $skill_path"
  else
    fail "plugin.json ref missing: $skill_path"
  fi
done

# 3. No hardcoded absolute paths in skills or rules
echo ""
echo "--- Checking for hardcoded paths ---"
if grep -rl 'wsl\.localhost' "$PLUGIN_DIR/skills/" "$PLUGIN_DIR/rules/" 2>/dev/null; then
  fail "Found hardcoded WSL paths in skills/rules"
else
  pass "No hardcoded WSL paths"
fi

if grep -rl 'SocietyManagement' "$PLUGIN_DIR/skills/" "$PLUGIN_DIR/rules/" 2>/dev/null; then
  fail "Found project-specific 'SocietyManagement' references"
else
  pass "No project-specific references"
fi

# 4. Check qa-workflow plugin too (if present)
QA_DIR="$REPO_ROOT/plugins/qa-workflow"
if [ -d "$QA_DIR" ]; then
  echo ""
  echo "=== QA-Workflow Smoke Tests ==="

  for skill in "$QA_DIR"/skills/*/SKILL.md; do
    name=$(basename "$(dirname "$skill")")
    if head -20 "$skill" | grep -q '^name:'; then
      pass "qa/$name: has 'name' field"
    else
      fail "qa/$name: missing 'name' field"
    fi
  done

  if python3 -c "import json; json.load(open('$QA_DIR/plugin.json'))" 2>/dev/null; then
    pass "qa-workflow plugin.json is valid JSON"
  else
    fail "qa-workflow plugin.json is not valid JSON"
  fi

  if grep -rl 'wsl\.localhost\|SocietyManagement' "$QA_DIR/skills/" 2>/dev/null; then
    fail "Found hardcoded paths in qa-workflow"
  else
    pass "No hardcoded paths in qa-workflow"
  fi
fi

echo ""
if [ $FAIL -eq 0 ]; then
  echo "🎉 All smoke tests passed!"
else
  echo "💥 Some smoke tests failed."
  exit 1
fi
