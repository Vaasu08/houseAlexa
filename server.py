"""
server.py - Self-Hosted Dynamic MCP Server for houseAlexa
Conforms to: MCP Spec (Streamable HTTP transport) for Alexa+ & MCP Apps SDK

MCP App Architecture:
Combines MCP tools with interactive UI resources:
1. UI Resource (`ui://house-alexa/dashboard.html`): Serves bundled interactive HTML dashboard.
2. Tool Linking (`_meta.ui.resourceUri`): Tools link directly to the UI view for Claude Desktop & Alexa+ smart screens.
3. Fallback for non-UI hosts: Full text/JSON data returned for voice-only Echo speakers.
4. Dynamic Entity Controller: Controls any device or auto-registers new appliances on the fly.
"""

import sys
import os
import json
import argparse
from typing import Optional, Dict, Any
from mcp.server.mcpserver import MCPServer
from house_state import house

# 1. Create the MCP Server
mcp_server = MCPServer(
    name="house-alexa-mcp",
    version="2.0.0",
    description="Dynamic AI-first smart home control server & MCP App for Alexa+ and Claude Desktop.",
)

DASHBOARD_HTML_PATH = os.path.join(os.path.dirname(__file__), "ui", "dashboard.html")


def load_dashboard_html() -> str:
    if os.path.exists(DASHBOARD_HTML_PATH):
        with open(DASHBOARD_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<html><body><h1>houseAlexa Dashboard</h1></body></html>"


# 2. Live MCP Data Resource: Real-time context feed for LLM prompts
@mcp_server.resource("house://devices")
def live_devices_state() -> str:
    """Live state of all devices and appliances in the home."""
    return json.dumps(house.get_summary(), indent=2)


# 3. Interactive MCP App UI Resource (Serves bundled HTML UI view)
@mcp_server.resource(
    "ui://house-alexa/dashboard.html",
    name="Smart Home Interactive Dashboard",
    title="houseAlexa Interactive View",
    description="Interactive MCP App UI for controlling smart home devices and viewing live status.",
    mime_type="text/html",
    meta={
        "ui": {
            "csp": {
                "defaultSrc": ["'self'"],
                "scriptSrc": ["'self'", "'unsafe-inline'"],
                "styleSrc": ["'self'", "'unsafe-inline'"],
            }
        }
    },
)
def interactive_dashboard_ui() -> str:
    """Returns the bundled interactive MCP App HTML UI."""
    return load_dashboard_html()


# 4. Dynamic AI Tools with linked MCP App UI Views
UI_META = {"ui": {"resourceUri": "ui://house-alexa/dashboard.html"}}


@mcp_server.tool(
    name="open_dashboard",
    description="Open the interactive smart home dashboard UI inside Claude Desktop or Alexa+ smart display screens.",
    meta=UI_META,
)
def open_dashboard() -> dict:
    """Returns current home state and launches the interactive MCP App dashboard."""
    return {
        "status": "ready",
        "message": "Interactive Smart Home Dashboard launched.",
        "devices": house.get_summary(),
    }


@mcp_server.tool(
    name="get_devices",
    description="Inspect smart home devices. Returns all devices or filters by category (lighting, climate, security, media, appliance) or room (living_room, bedroom, kitchen, garage).",
    meta=UI_META,
)
def get_devices(filter: Optional[str] = None) -> dict:
    """Inspect smart home devices.

    Args:
        filter: Optional keyword to filter devices by room or category (e.g. 'bedroom', 'lighting', 'security').
    """
    return house.get_devices(filter_query=filter)


@mcp_server.tool(
    name="control_device",
    description="Dynamically control or set properties on any device in the home. Works for existing devices (lights, thermostat, doors, garage, speakers) AND new appliances (robot_vacuum, coffee_maker, oven, sprinklers) without hardcoding.",
    meta=UI_META,
)
def control_device(
    device_id: str,
    updates: dict,
) -> dict:
    """Dynamically control any smart device.

    Args:
        device_id: Name or ID of the device (e.g. 'bedroom_light', 'thermostat', 'front_door', 'garage_door', 'robot_vacuum').
        updates: Key-value dictionary of desired properties (e.g. {'power': True, 'brightness': 80}, {'locked': False}, {'open': True}, {'status': 'cleaning'}).
    """
    return house.update_device(device_id=device_id, updates=updates)


@mcp_server.tool(
    name="apply_scene",
    description="Activate a multi-device scene (e.g. 'bedtime', 'leaving_home', 'movie_night', 'good_morning') or apply a batch update across multiple devices in one single call.",
    meta=UI_META,
)
def apply_scene(
    scene_name: Optional[str] = None,
    batch_updates: Optional[dict] = None,
) -> dict:
    """Trigger a home routine or batch update.

    Args:
        scene_name: Built-in scene name ('bedtime', 'leaving_home', 'movie_night', 'good_morning').
        batch_updates: Optional dictionary mapping device IDs to their updates (e.g. {'bedroom_light': {'power': False}, 'front_door': {'locked': True}}).
    """
    if scene_name:
        return house.activate_scene(scene_name)
    elif batch_updates:
        return house.batch_update(batch_updates)
    else:
        return {"error": "Please provide either scene_name or batch_updates."}


def main():
    parser = argparse.ArgumentParser(description="houseAlexa MCP Server & App")
    parser.add_argument(
        "--transport",
        choices=["streamable-http", "sse", "stdio"],
        default="streamable-http",
        help="MCP transport protocol. Default is 'streamable-http' for Alexa+.",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host address to bind HTTP server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to run HTTP server on")
    parser.add_argument(
        "--path",
        default="/mcp",
        help="Streamable HTTP endpoint path (default: /mcp)",
    )

    args = parser.parse_args()

    print("=" * 60)
    print(" [HOUSE] houseAlexa Dynamic MCP App Server (v2.0)")
    print(f" Transport: {args.transport}")
    if args.transport in ("streamable-http", "sse"):
        print(f" Listening on: http://{args.host}:{args.port}{args.path}")
    print(" UI Resource: ui://house-alexa/dashboard.html")
    print("=" * 60)

    if args.transport == "streamable-http":
        mcp_server.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            streamable_http_path=args.path,
        )
    elif args.transport == "sse":
        mcp_server.run(
            transport="sse",
            host=args.host,
            port=args.port,
        )
    else:
        mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
