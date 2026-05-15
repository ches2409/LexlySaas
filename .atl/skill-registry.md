# Skill Registry — lexlysaas

> Generated: 2026-05-11 | Mode: engram

## Project Context

- **Stack**: FastAPI + Python 3.13 + SQLModel + Supabase
- **Goal**: Clean Architecture / Hexagonal Architecture
- **Persistence**: Engram only (no openspec/)

---

## Core Skills

### fastapi-pro
**Path**: `~/.config/opencode/skills/fastapi-pro/SKILL.md`
**Trigger**: When developing FastAPI applications, APIs.
**Compact Rules**:
- Write async-first code by default
- Use Pydantic V2 for data validation (not BaseModel)
- Implement Repository pattern for database access
- Use dependency injection with `Depends()`
- Write tests with pytest-asyncio and TestClient
- Configure proper CORS and security headers

### python-pro
**Path**: `~/.config/opencode/skills/python-pro/SKILL.md`
**Trigger**: When developing in Python.
**Compact Rules**:
- Use Python 3.13 features (better error messages, perf)
- Use uv for package management (faster than pip)
- Use ruff for linting AND formatting (replaces black/isort/flake8)
- Add type hints everywhere; use mypy for checking
- Use Pydantic for data validation (not dataclasses for API input)
- Profile with py-spy before optimizing

### sql-pro
**Path**: `~/.config/opencode/skills/sql-pro/SKILL.md`
**Trigger**: When writing SQL queries, database design.
**Compact Rules**:
- Use asyncpg with SQLModel for async DB access
- Write parameterized queries (no string interpolation)
- Use connection pooling (asyncpg pool)
- Index foreign keys and frequently queried columns
- Use EXPLAIN ANALYZE for query debugging

### supabase-automation
**Path**: `~/.config/opencode/skills/supabase-automation/SKILL.md`
**Trigger**: Any Supabase task (database, auth, edge functions).
**Compact Rules**:
- Use Supabase MCP tools for DB operations
- Write migrations in SQL (not ORM)
- Enable RLS on all tables
- Test migrations locally before production

### architecture-patterns
**Path**: `~/.config/opencode/skills/architecture-patterns/SKILL.md`
**Trigger**: When designing backend architecture.
**Compact Rules**:
- Use Clean Architecture layers: API → Service → Repository → Model
- Keep domain logic in services (not in API routes)
- Use dependency injection for testability
- Extract to repositories for database access

### clean-code
**Path**: `~/.config/opencode/skills/clean-code/SKILL.md`
**Trigger**: When refactoring or writing new code.
**Compact Rules**:
- Functions < 20 lines
- Names reveal intent (no `tmp`, `data`, `stuff`)
- Single responsibility per module
- DRY: extract repeated logic
- Comments explain WHY, not WHAT

### systematic-debugging
**Path**: `~/.config/opencode/skills/systematic-debugging/SKILL.md`
**Trigger**: Any bug, test failure, or unexpected behavior.
**Compact Rules**:
- Never propose fixes before identifying root cause
- Isolate: reproduce in minimal case
- Trace: symptoms → root cause
- Verify: test fixes thoroughly

---

## SDD Workflow Skills

### sdd-explore
**Path**: `~/.config/opencode/skills/sdd-explore/SKILL.md`
**Trigger**: Exploring SDD ideas before committing to a change.

### sdd-propose
**Path**: `~/.config/opencode/skills/sdd-propose/SKILL.md`
**Trigger**: Creating an SDD change proposal.

### sdd-spec
**Path**: `~/.config/opencode/skills/sdd-spec/SKILL.md`
**Trigger**: Writing SDD delta specs.

### sdd-design
**Path**: `~/.config/opencode/skills/sdd-design/SKILL.md`
**Trigger**: Creating SDD technical design.

### sdd-tasks
**Path**: `~/.config/opencode/skills/sdd-tasks/SKILL.md`
**Trigger**: Breaking SDD change into implementation tasks.

### sdd-apply
**Path**: `~/.config/opencode/skills/sdd-apply/SKILL.md`
**Trigger**: Implementing SDD tasks from specs.

### sdd-verify
**Path**: `~/.config/opencode/skills/sdd-verify/SKILL.md`
**Trigger**: SDD verification phase.

### sdd-archive
**Path**: `~/.config/opencode/skills/sdd-archive/SKILL.md`
**Trigger**: Archiving completed SDD change.

---

## Quality Tools

### lint-and-validate
**Path**: `~/.config/opencode/skills/lint-and-validate/SKILL.md`
**Trigger**: Run after EVERY code change.
**Compact Rules**:
- Run linter before commit (ruff check)
- Run type checker (mypy)
- Run tests before push
- Never skip validation to "save time"

---

## Notes

- This project needs: pytest, ruff, mypy configuration
- Frontend is vanilla JS (not React/Next.js yet)
- Backend follows layered architecture (api → services → models)
- Database: Supabase with SQLModel