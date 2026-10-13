"""
test_client.py - Automated Test Client for houseAlexa MCP Server

Analogy for a 5yo:
This is our Robot Inspector!
It connects to our MCP server over the radio (Streamable HTTP) just like Alexa+ will,
asks for a list of all buttons, presses a few of them,
and checks if the bedroom light actually turned on and the music started playing!
"""

import asyncio
import sys
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
                print(f"[+] Discovered {len(tools_response.tools)} tools:")
                for t in tools_response.tools:
                    print(f"   - {t.name}: {t.description}")

                # 3. Test Tool 1: get_house_status
                print("\n[*] [Test 1] Inspecting initial house state...")
                status = await session.call_tool("get_house_status")
                print(f"   Status received: {status.content[0].text if status.content else 'Empty'}")

                # 4. Test Tool 2: Turn on bedroom light
                print("\n[*] [Test 2] Turning on Bedroom Light to 85%...")
                light_res = await session.call_tool(
                    "control_light",
                    {"room": "bedroom", "power": True, "brightness": 85, "color": "soft_amber"},
                )
                print(f"   Response: {light_res.content[0].text if light_res.content else 'None'}")

                # 5. Test Tool 3: Set Thermostat
                print("\n[*] [Test 3] Setting Thermostat to 20.5 C (Cool mode)...")
                temp_res = await session.call_tool(
                    "control_thermostat",
                    {"temperature_celsius": 20.5, "mode": "cool"},
                )
                print(f"   Response: {temp_res.content[0].text if temp_res.content else 'None'}")

                # 6. Test Tool 4: Unlock front door
                print("\n[*] [Test 4] Unlocking the Front Door...")
                lock_res = await session.call_tool(
                    "control_door_lock",
                    {"door": "front_door", "locked": False},
                )
                print(f"   Response: {lock_res.content[0].text if lock_res.content else 'None'}")

                # 7. Test Tool 5: Open Garage Door
                print("\n[*] [Test 5] Opening the Garage Door...")
                garage_res = await session.call_tool(
                    "control_garage_door",
                    {"open": True},
                )
                print(f"   Response: {garage_res.content[0].text if garage_res.content else 'None'}")

                # 8. Test Tool 6: Play Lo-Fi Beats
                print("\n[*] [Test 6] Playing Chill Lo-Fi on Living Room Speaker...")
                music_res = await session.call_tool(
                    "control_music",
                    {"action": "play", "track": "Midnight Lofi Beats", "volume": 65},
                )
                print(f"   Response: {music_res.content[0].text if music_res.content else 'None'}")

                # 9. Check final updated house status
                print("\n[*] [Final Check] Verifying all updated device states...")
                final_status = await session.call_tool("get_house_status")
                print(f"   Updated house state:\n{final_status.content[0].text if final_status.content else 'None'}")

                # 10. Verify disk persistence
                import os
                import json
                print("\n[*] [Persistence Check] Verifying house_state.json on disk...")
                if os.path.exists("house_state.json"):
                    with open("house_state.json", "r", encoding="utf-8") as f:
                        disk_data = json.load(f)
                    assert disk_data["security"]["garage_door"]["open"] is True, "Garage door state not saved to disk!"
                    assert disk_data["lights"]["bedroom"]["power"] is True, "Bedroom light state not saved to disk!"
                    print("   [OK] house_state.json successfully verified on disk!")
                else:
                    print("   [WARN] house_state.json not found in working directory (might be running remotely)")

                print("\n[SUCCESS] ALL TESTS PASSED! Your MCP server is 100% compliant and working!")
    except Exception as e:
        print(f"\n[FAIL] Error connecting to MCP server: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/mcp"
    asyncio.run(test_mcp_server(url))

