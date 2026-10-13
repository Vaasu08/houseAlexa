# Project: houseAlexa MCP Server

## Vision
A self-hosted Model Context Protocol (MCP) server for Alexa+ integrations and smart home AI agents, conforming to the Alexa+ 2025-11-25 Streamable HTTP specification.

## Core Architecture
- **Transport**: Streamable HTTP (`/mcp` endpoint) on port `8000`, with fallback support for SSE and stdio.
- **State Engine**: Virtual smart home device state in `house_state.py` with disk persistence (`house_state.json`).
- **MCP Server Layer**: Python `mcp` SDK exposing tools with structured schemas and human-readable feedback.
- **Test Harness**: `test_client.py` and `pytest` integration test suite.

## Tech Stack
- Python 3.12+
- `mcp` (v2.3.0+)
- `uvicorn`, `starlette`, `httpx`
- `pydantic` v2
