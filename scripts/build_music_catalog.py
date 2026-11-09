#!/usr/bin/env python3
"""Regenerate data/music-catalog.json from the Artispreneur music-layer source.

Source of truth: ~/workspace/artispreneur-music-layer/catalog.yaml
(88 skills, 7 agents, 5 workflows). This script copies NOTHING but metadata
(name/title/agent/category/status/path/extends) -- draft skill BODIES are
never copied into this package; only the one active skill's body is shipped
(see skills-artispreneur/pro-registration.md, copied by hand with provenance).

Run from the package root:  python3 scripts/build_music_catalog.py
Idempotent. Exits non-zero if the source count is not 88 or the active
count is not 1, so drift is caught instead of silently shipped.
"""
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.expanduser(
    "~/workspace/artispreneur-music-layer/catalog.yaml")
OUT = os.path.join(HERE, "data", "music-catalog.json")


def main():
    with open(SRC, encoding="utf-8") as f:
        cat = yaml.safe_load(f)
    skills = cat.get("skills", [])
    agents = {}
    for s in skills:
        agents.setdefault(s["agent"], []).append(s["name"])
    out = {
        "source": "artispreneur-music-layer/catalog.yaml",
        "registry_version": cat.get("registry_version"),
        "counts": cat.get("counts"),
        "skills": [
            {
                "slug": s["name"],
                "name": s.get("title") or s["name"],
                "description": s.get("title") or "",
                "category": s.get("category") or "music",
                "agent": s.get("agent"),
                "status": s.get("status"),
                "extends": s.get("extends"),
                "source_path": "artispreneur-music-layer/" + (s.get("path") or ""),
            }
            for s in skills
        ],
        "agents": [
            {"slug": a, "skill_count": len(v), "skills": sorted(v)}
            for a, v in sorted(agents.items())
        ],
    }
    active = [s for s in out["skills"] if s["status"] == "active"]
    draft = [s for s in out["skills"] if s["status"] == "draft"]
    print("music skills: %d (active %d, draft %d, agents %d)"
          % (len(out["skills"]), len(active), len(draft), len(out["agents"])))
    print("active: %s" % [s["slug"] for s in active])
    if len(out["skills"]) != 88:
        print("ERROR: expected 88 music skills, got %d -- source drifted"
              % len(out["skills"]), file=sys.stderr)
        sys.exit(1)
    if len(active) != 1 or active[0]["slug"] != "pro-registration":
        print("ERROR: expected exactly one active skill (pro-registration), "
              "got %s" % [s["slug"] for s in active], file=sys.stderr)
        sys.exit(1)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
