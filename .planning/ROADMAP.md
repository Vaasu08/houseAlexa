# Roadmap: houseAlexa MCP Server

## Milestone 1: Production Baseline & Resilience

- **Phase 01: Core Tools & State Persistence**
  - **Objective**: Implement garage door control tool, fix lock validation, add disk-based state persistence (`house_state.json`), and update test client.
  - **Status**: Ready to execute
  - **Key Deliverables**:
    - `control_garage_door` tool in `server.py` and `house_state.py`
    - `set_lock` validation fix
    - JSON persistence with automatic save/load
    - Extended `test_client.py` test suite

- **Phase 02: Authentication & Security Hardening**
  - **Objective**: Add Bearer token / API key authentication to Streamable HTTP endpoints and provide ngrok configuration documentation.
  - **Status**: Backlog

- **Phase 03: Pytest Automated Verification Suite**
  - **Objective**: Full automated unit test suite with mock fixtures and CI-ready test runs.
  - **Status**: Backlog
