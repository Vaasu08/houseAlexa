---
phase: "01"
name: "Core Tools & State Persistence"
status: "completed"
wave_count: 2
---

# Phase 01 Plan: Core Tools & State Persistence

## Objective
Implement missing device control tools (garage door), correct device schema validation bugs, add robust local disk persistence (`house_state.json`), and verify everything via the test client.

---

## Wave 1: State Engine Enhancements & Persistence

### Task 1.1: Add Garage Door Control & Lock Validation in `house_state.py`
- **File**: `house_state.py`
- **Changes**:
  1. Add `set_garage_door(open: bool) -> str` method.
  2. Fix `set_lock` to only allow actual doors (`front_door`, `back_door`) and reject invalid doors or garage door.
  3. Ensure clean human-readable responses.

### Task 1.2: Add Disk Persistence to `HouseState`
- **File**: `house_state.py`
- **Changes**:
  1. Add `save_to_disk(filepath: str = "house_state.json")`.
  2. Add `load_from_disk(filepath: str = "house_state.json")`.
  3. Call `save_to_disk()` automatically after every modifying action (`set_light`, `set_thermostat`, `set_lock`, `set_garage_door`, `control_media`).

---

## Wave 2: MCP Server Tool Exposure & Test Client Verification

### Task 2.1: Expose `control_garage_door` in `server.py`
- **File**: `server.py`
- **Changes**:
  1. Add `@mcp_server.tool(name="control_garage_door", description="...")`.
  2. Map parameters: `open: bool` to `house.set_garage_door(open)`.

### Task 2.2: Update and Verify with `test_client.py`
- **File**: `test_client.py`
- **Changes**:
  1. Add step to test `control_garage_door(open=True)`.
  2. Verify that `house_state.json` is created and contains the updated state.
  3. Verify round-trip test against a running MCP server.

---

## Acceptance Criteria
- [x] Server exposes 6 tools instead of 5 (`get_house_status`, `control_light`, `control_thermostat`, `control_door_lock`, `control_garage_door`, `control_music`).
- [x] `house_state.json` is automatically updated on disk whenever any tool is invoked.
- [x] Server reload preserves device state from disk instead of resetting to defaults.
- [x] `test_client.py` executes all 6 tool tests and exits with code 0.

