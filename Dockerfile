# Artispreneur MCP + REST API -- local runner image.
# Stdlib only: no pip installs, no requirements.txt.
FROM python:3.12-slim
WORKDIR /app
# NOTE: entitlements.json is NEVER copied into this image (see .dockerignore).
# It holds DEMO keys for local smoke tests only. In production, auth is the
# MCP_AUTH_TOKEN env var (admin) plus the Supabase has_access() lookup that
# replaces demo entitlements at go-live (see GO-LIVE-CHECKLIST.md).
COPY server.py ./
COPY api ./api
COPY skills ./skills
COPY skills-artispreneur ./skills-artispreneur
COPY skills-index.json ./
COPY data ./data
COPY packs.json ./
COPY agents.json ./
# HOST=0.0.0.0 is set explicitly HERE ONLY (inside the container). The
# server default stays 127.0.0.1 (QA W-2 fix) -- never 0.0.0.0 by default
# on a developer machine.
# Render injects PORT at runtime (overrides the 8787 default in server.py);
# do NOT hardcode PORT here, or a Render-assigned port would be ignored.
ENV HOST=0.0.0.0
EXPOSE 8787
CMD ["python3", "server.py"]
