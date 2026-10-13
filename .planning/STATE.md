# Project State

## Active Milestone
- Milestone 1: Production Baseline & Resilience

## Current Phase
- Phase 01: Core Tools & State Persistence
- Status: Completed (Verified with test_client.py)
- Next Phase: Phase 02: Authentication & Security Hardening (or /gsd-code-review 1)


## Key Decisions
- **Persistence**: Using JSON file (`house_state.json`) with auto-sync on mutation for simplicity, zero extra dependencies, and ease of inspection.
- **Protocol**: Streamable HTTP on `/mcp` (Alexa+ 2025-11-25 standard).
