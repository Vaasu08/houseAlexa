---
name: create-mcp-app
description: "Build interactive UIs that run inside MCP-enabled hosts like Claude Desktop or Alexa+ with screens. An MCP App combines an MCP tool with an HTML resource to display rich, interactive content."
---

# Create MCP App

Build interactive UIs that run inside MCP-enabled hosts like Claude Desktop. An MCP App combines an MCP tool with an HTML resource to display rich, interactive content.

## Core Concept: Tool + Resource

Every MCP App requires two parts linked together:

1. **Tool** - Called by the LLM/host, returns data
2. **Resource** - Serves the bundled HTML UI that displays the data

The tool's `_meta.ui.resourceUri` references the resource's URI.

Host calls tool → Host renders resource UI → Server returns result → UI receives result.

## Quick Start Decision Tree

### Framework Selection

| Framework | SDK Support | Best For |
|-----------|-------------|----------|
| React | `useApp` hook provided | Teams familiar with React |
| Vanilla JS | Manual lifecycle | Simple apps, no build complexity |
| Vue/Svelte/Preact/Solid | Manual lifecycle | Framework preference |

### Project Context

**Adding to existing MCP server:**
- Add tool registration with `_meta.ui.resourceUri`
- Add resource registration serving bundled HTML with `_meta.ui.csp`
- Ensure text fallback in `content` array for non-UI hosts

## Critical Implementation Notes

1. **No text fallback** - Always provide text content array for non-UI hosts.
2. **Missing CSP configuration** - MCP Apps HTML is served as an MCP resource with no same-origin server; ALL network requests require CSP configuration in `_meta.ui.csp`.
3. **CSP or CORS config in resource metadata** - `_meta.ui.csp` and `_meta.ui.domain` go in the resource metadata.
4. **Handlers before app.connect()** - Register ALL handlers before calling `app.connect()`.
