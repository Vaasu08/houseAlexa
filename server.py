"""
server.py - Self-Hosted Dynamic MCP Server for houseAlexa
Conforms to: MCP Spec (Streamable HTTP transport) for Alexa+

AI-First Architecture:
Rather than hardcoding separate tools for every device, this server exposes:
1. Dynamic Controller (`control_device`): Control any existing or newly added device.
2. Device Inspector (`get_devices`): Inspect all devices or filter by category/room.
3. Macro Scene Activator (`apply_scene`): Execute multi-device routines in a single call.
4. Live Context Resource (`house://devices`): Live prompt context for Alexa+.
"""

import sys
import json
import argparse
from typing import Optional, Dict, Any
from mcp.server.mcpserver import MCPServer
from house_state import house

# 1. Create the MCP Server
mcp_server = MCPServer(
    name="house-alexa-mcp",
    version="2.0.0",
    description="Dynamic AI-first smart home control server for Alexa+ integrations via Model Context Protocol.",
)

# 2. Live MCP Resource: Alexa+ has the live home state streamed directly into prompt context
@mcp_server.resource("house://devices")
def live_devices_state() -> str:
    """Live state of all devices and appliances in the home."""
    return json.dumps(house.get_summary(), indent=2)


# 3. Dynamic AI Tools
@mcp_server.tool(
    name="get_devices",
    description="Inspect smart home devices. Returns all devices or filters by category (lighting, climate, security, media, appliance) or room (living_room, bedroom, kitchen, garage).",
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
    parser = argparse.ArgumentParser(description="houseAlexa MCP Server")
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
    print(" [HOUSE] houseAlexa Dynamic MCP Server (Alexa+ Spec v2.0)")
    print(f" Transport: {args.transport}")
    if args.transport in ("streamable-http", "sse"):
        print(f" Listening on: http://{args.host}:{args.port}{args.path}")
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
