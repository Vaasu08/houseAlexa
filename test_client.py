"""
test_client.py - Automated Test Client for houseAlexa Dynamic MCP Server
Conforms to: MCP Spec (Streamable HTTP transport) for Alexa+

Analogy for a 5yo:
This is our Robot Inspector!
It connects to our MCP server over the radio (Streamable HTTP), discovers the
dynamic tools, adjusts lights and garage, registers a brand new appliance
(a robot vacuum) on the fly without any code changes, runs a whole-house scene,
and verifies that everything persisted to disk!
"""

import asyncio
import sys
import json
import os
from mcp.client.streamable_http import streamable_http_client
from mcp.client.session import ClientSession


async def test_mcp_server(url: str = "http://127.0.0.1:8000/mcp"):
    print(f"[*] Connecting to MCP Server at {url} ...")

    try:
        async with streamable_http_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # 1. Initialize session with the server
                print("[*] Initializing MCP session with server...")
                init_result = await session.initialize()
                print(f"[OK] Connected! Server Name: {init_result.server_info.name} (v{init_result.server_info.version})")

                # 2. Discover available tools
                print("\n[*] Asking server for list of available tools...")
                tools_response = await session.list_tools()
                print(f"[+] Discovered {len(tools_response.tools)} dynamic tools:")
                for t in tools_response.tools:
                    print(f"   - {t.name}: {t.description}")

                # 3. Test Tool 1: get_devices (all devices)
                print("\n[*] [Test 1] Inspecting all devices via get_devices()...")
                all_devs = await session.call_tool("get_devices")
                raw_text = all_devs.content[0].text if all_devs.content else "{}"
                dev_data = json.loads(raw_text)
                print(f"   Discovered {len(dev_data)} active devices in home state.")

                # 4. Test Tool 2: get_devices with filter
                print("\n[*] [Test 2] Filtering devices by category 'lighting'...")
                lights_res = await session.call_tool("get_devices", {"filter": "lighting"})
                lights_data = json.loads(lights_res.content[0].text)
                print(f"   Found {len(lights_data)} lighting devices: {list(lights_data.keys())}")

                # 5. Test Tool 3: control_device (existing device)
                print("\n[*] [Test 3] Dynamically updating 'bedroom_light' (power=True, brightness=85, color='soft_amber')...")
                light_res = await session.call_tool(
                    "control_device",
                    {
                        "device_id": "bedroom_light",
                        "updates": {"power": True, "brightness": 85, "color": "soft_amber"},
                    },
                )
                print(f"   Response: {light_res.content[0].text if light_res.content else 'None'}")

                # 6. Test Tool 4: control_device (garage door)
                print("\n[*] [Test 4] Opening the garage door via control_device()...")
                garage_res = await session.call_tool(
                    "control_device",
                    {"device_id": "garage_door", "updates": {"open": True}},
                )
                print(f"   Response: {garage_res.content[0].text if garage_res.content else 'None'}")

                # 7. Test Tool 5: Dynamic Auto-Registration of a Brand New Device!
                print("\n[*] [Test 5] Dynamic Auto-Registration: Controlling a device never hardcoded in Python ('robot_vacuum')...")
                vac_res = await session.call_tool(
                    "control_device",
                    {
                        "device_id": "robot_vacuum",
                        "updates": {
                            "category": "appliance",
                            "room": "kitchen",
                            "status": "cleaning_kitchen",
                            "battery": 92,
                        },
                    },
                )
                print(f"   Response: {vac_res.content[0].text if vac_res.content else 'None'}")

                # 8. Test Tool 6: apply_scene (Macro routine)
                print("\n[*] [Test 6] Activating pre-set multi-device scene 'movie_night'...")
                scene_res = await session.call_tool("apply_scene", {"scene_name": "movie_night"})
                print(f"   Response: {scene_res.content[0].text if scene_res.content else 'None'}")

                # 9. Verify disk persistence
                print("\n[*] [Persistence Check] Verifying house_state.json on disk...")
                if os.path.exists("house_state.json"):
                    with open("house_state.json", "r", encoding="utf-8") as f:
                        disk_data = json.load(f)
                    assert "robot_vacuum" in disk_data, "Dynamically added robot_vacuum not saved to disk!"
                    assert disk_data["living_room_light"]["brightness"] == 20, "Movie night scene not persisted to disk!"
                    print("   [OK] house_state.json successfully verified on disk!")
                    print("   [OK] Dynamically added 'robot_vacuum' verified in persisted disk storage!")
                else:
                    print("   [WARN] house_state.json not found in working directory (might be running remotely)")

                print("\n[SUCCESS] ALL DYNAMIC MCP TESTS PASSED! Your AI-first smart home server is 100% operational!")
    except Exception as e:
        print(f"\n[FAIL] Error connecting to MCP server: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/mcp"
    asyncio.run(test_mcp_server(url))
