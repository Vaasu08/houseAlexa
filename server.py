"""
server.py - Self-Hosted MCP Server for houseAlexa
Conforms to: MCP Spec (Streamable HTTP transport) for Alexa+

Analogy for a 5yo:
This is the Walkie-Talkie Base Station!
Whenever a Brain (Alexa+, Claude, or a local robot) calls in over the radio,
this file answers the call and pushes the buttons on our Lego House.
"""

import sys
import argparse
from mcp.server.mcpserver import MCPServer
from house_state import house

# 1. Create the MCP Server
mcp_server = MCPServer(
    name="house-alexa-mcp",
    version="1.0.0",
    description="Smart home control server for Alexa+ integrations via Model Context Protocol.",
)


# 2. Add the buttons (Tools) that the AI Brain can press


@mcp_server.tool(
    name="get_house_status",
    description="Inspect the entire house to see what lights are on, current temperature, door locks, and music status.",
)
def get_house_status() -> dict:
    """Returns the current state of all devices in the house."""
    return house.get_summary()


@mcp_server.tool(
    name="control_light",
    description="Turn a light on or off in a specific room (living_room, bedroom, kitchen), and adjust brightness (0-100) or color.",
)
def control_light(
    room: str,
    power: bool,
    brightness: int = 100,
    color: str = None,
) -> str:
    """Control a room light.

    Args:
        room: Name of the room (living_room, bedroom, kitchen).
        power: True to turn ON, False to turn OFF.
        brightness: Brightness level from 0 to 100 percent.
        color: Optional color name (e.g. warm_white, blue, red).
    """
    return house.set_light(room=room, power=power, brightness=brightness, color=color)


@mcp_server.tool(
    name="control_thermostat",
    description="Set the target house temperature in Celsius and choose the HVAC mode (cool, heat, eco, fan, off).",
)
def control_thermostat(
    temperature_celsius: float,
    mode: str = "cool",
) -> str:
    """Control house AC/Heating.

    Args:
        temperature_celsius: Target temperature in degrees Celsius (e.g., 21.5).
        mode: HVAC mode (cool, heat, eco, fan, off).
    """
    return house.set_thermostat(target_c=temperature_celsius, mode=mode)


@mcp_server.tool(
    name="control_door_lock",
    description="Lock or unlock a specific entrance door (front_door, back_door).",
)
def control_door_lock(
    door: str,
    locked: bool,
) -> str:
    """Lock or unlock a house door.

    Args:
        door: The door name (front_door, back_door).
        locked: True to lock 🔒, False to unlock 🔓.
    """
    return house.set_lock(door=door, locked=locked)


@mcp_server.tool(
    name="control_garage_door",
    description="Open or close the garage door.",
)
def control_garage_door(
    open: bool,
) -> str:
    """Open or close the garage door.

    Args:
        open: True to open 🚪, False to close.
    """
    return house.set_garage_door(open=open)


@mcp_server.tool(
    name="control_music",
    description="Control the living room speaker: play a song, pause music, or set the volume (0-100).",
)
def control_music(
    action: str,
    track: str = "Chill Beats",
    volume: int = 50,
) -> str:
    """Control the music speaker.

    Args:
        action: One of 'play', 'pause', 'stop', 'volume'.
        track: Song or playlist title to play.
        volume: Volume level from 0 to 100 (when action='volume').
    """
    return house.control_media(action=action, track=track, volume=volume)


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
    print(" [HOUSE] houseAlexa MCP Server (Alexa+ Spec)")
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
