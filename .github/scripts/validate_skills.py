#!/usr/bin/env python3
"""Validate every skill directory: SKILL.md + frontmatter (skill-creator spec).

Run from the repository root:  python3 .github/scripts/validate_skills.py
"""
import sys
import re
from pathlib import Path
import yaml

ALLOWED = {'name', 'description', 'license', 'allowed-tools', 'metadata'}


def validate(p: Path):
    md = p / 'SKILL.md'
    if not md.exists():
        return False, "SKILL.md not found"
    content = md.read_text(encoding='utf-8', errors='replace')
    if not content.startswith('---'):
        return False, "No YAML frontmatter"
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return False, "Invalid frontmatter format"
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return False, f"YAML error: {e}"
    if not isinstance(fm, dict):
        return False, "Frontmatter must be a dict"
    extra = set(fm.keys()) - ALLOWED
    if extra:
        return False, f"Unexpected key(s): {sorted(extra)} (allowed: {sorted(ALLOWED)})"
    if not fm.get('name') or not fm.get('description'):
        return False, "name and description are required"
    if fm['name'] != p.name:
        return False, f"name '{fm['name']}' != directory '{p.name}'"
    return True, "OK"


def main():
    ok = fail = 0
    for d in sorted(Path('.').iterdir()):
        if not d.is_dir() or d.name.startswith('.'):
            continue
        v, msg = validate(d)
        print(f"[{'PASS' if v else 'FAIL'}] {d.name}: {msg}")
        ok += 1 if v else 0
        fail += 0 if v else 1
    print(f"\nTotal: {ok} passed, {fail} failed")
    sys.exit(1 if fail else 0)


if __name__ == '__main__':
    main()
