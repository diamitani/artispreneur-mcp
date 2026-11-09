#!/usr/bin/env python3
"""Rebuild skills-index.json from disk (~/workspace/skill-library).

For each skill directory (excluding .git, _overwritten-rostr-originals,
_tools, dist) the SKILL.md is copied to skills/<slug>.md and indexed with
slug, name, description, category and sha256 of the copied file.

Name/description/category for the 384 audited skills are taken from the
skill-co-mcp index (whose sha256 values are re-verified against the copied
files here -- any drift fails loudly). grok-social-cleanup (#385) is indexed
from its own frontmatter; its frontmatter was audited 2026-11-07 (valid, no
secrets, keys are {{XAI_API_KEY}}/{{OPENROUTER_API_KEY}} placeholders).

Run from the package root:  python3 scripts/build_skills_index.py
Exits non-zero unless exactly 385 skills are indexed.
"""
import hashlib
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.expanduser("~/workspace/skill-library")
SKIP = {".git", "_overwritten-rostr-originals", "_tools", "dist"}
OLD_INDEX = os.path.expanduser(
    "~/workspace/skill-co-mcp/skills-index.json")


def _frontmatter(text):
    name, desc = None, None
    if text.startswith("---"):
        end = text.find("\n---", 3)
        head = text[3:end] if end != -1 else text
        m = re.search(r'^name:\s*["\']?(.*?)["\']?\s*$', head, re.M)
        if m:
            name = m.group(1).strip()
        m = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', head, re.M)
        if m:
            desc = m.group(1).strip()
    return name, desc


def main():
    old_by_slug = {}
    if os.path.exists(OLD_INDEX):
        with open(OLD_INDEX, encoding="utf-8") as f:
            old_by_slug = {e["slug"]: e for e in json.load(f)}
    slugs = sorted(d for d in os.listdir(LIB)
                   if os.path.isdir(os.path.join(LIB, d)) and d not in SKIP)
    index = []
    for slug in slugs:
        src = os.path.join(LIB, slug, "SKILL.md")
        if not os.path.exists(src):
            print("ERROR: missing SKILL.md: %s" % slug, file=sys.stderr)
            sys.exit(1)
        dst = os.path.join(HERE, "skills", slug + ".md")
        shutil.copyfile(src, dst)
        data = open(dst, "rb").read()
        sha = hashlib.sha256(data).hexdigest()
        name, desc = _frontmatter(data.decode("utf-8"))
        old = old_by_slug.get(slug)
        if old:
            if old["sha256"] != sha:
                print("ERROR: sha drift vs skill-co index: %s" % slug,
                      file=sys.stderr)
                sys.exit(1)
            cat = old.get("category") or "other"
            name = old.get("name") or name or slug
            desc = old.get("description") or desc or ""
        else:
            cat = "social-media"
            name = name or slug
            desc = desc or ""
        index.append({"slug": slug, "name": name, "description": desc,
                      "category": cat, "sha256": sha})
    if len(index) != 385:
        print("ERROR: expected 385 skills, got %d" % len(index),
              file=sys.stderr)
        sys.exit(1)
    with open(os.path.join(HERE, "skills-index.json"), "w",
              encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("skills-index.json: %d entries" % len(index))


if __name__ == "__main__":
    main()
