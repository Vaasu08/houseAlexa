# Requirements: houseAlexa MCP Server

## Milestone 1: Core Functionality & Persistence

### 1. Device Controls
- [ ] **REQ-DEV-01**: Implement `control_garage_door` tool to open and close `garage_door`.
- [ ] **REQ-DEV-02**: Fix `set_lock` door validation to prevent mutating non-door devices (e.g., garage door).
- [ ] **REQ-DEV-03**: Support strict parameter schemas (rooms: living_room, bedroom, kitchen; HVAC modes: off, cool, heat, fan, eco; brightness: 0-100; volume: 0-100).

### 2. State Persistence
- [ ] **REQ-STATE-01**: Auto-save house state to disk (`house_state.json`) upon device mutation.
- [ ] **REQ-STATE-02**: Load existing state from disk on startup, falling back to default configuration if file is missing.
- [ ] **REQ-STATE-03**: Thread-safe state access and mutations.

### 3. Verification & Testing
- [ ] **REQ-TEST-01**: Update `test_client.py` to test the new `control_garage_door` tool.
- [ ] **REQ-TEST-02**: Verify state persistence across server restarts in test suite.
