# Project State

## Active Milestone
- Milestone 1: Production Baseline & Resilience

## Current Phase
- Phase 01: Core Tools & State Persistence
- Status: Completed (Verified with test_client.py)
- Next Phase: Phase 02: Authentication & Security Hardening (or /gsd-code-review 1)


## Key Decisions
- **Architecture (v2.0)**: Transitioned from rigid per-device hardcoded tools to an AI-first Dynamic Entity Registry (`get_devices`, `control_device`, `apply_scene`, and `house://devices` resource). Supports auto-registering any new device dynamically without code changes.
- **Persistence**: Using JSON file (`house_state.json`) with auto-sync on mutation for simplicity, zero extra dependencies, and ease of inspection.
- **Protocol**: Streamable HTTP on `/mcp` (Alexa+ 2025-11-25 standard).

