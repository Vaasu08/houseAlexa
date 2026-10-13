# 🏠 Alexa+ Smart Home Tooling & Architectural Guide

This document captures the analysis, comprehensive tool catalog, and architectural paradigms for integrating smart home devices with **Alexa+** via the **Model Context Protocol (MCP)**.

---

## 1. 📌 Current Baseline: What is Implemented Today

Currently, the `houseAlexa` MCP server exposes **6 explicit tools** via Streamable HTTP:

| Current Tool | Target Domain | Purpose |
| :--- | :--- | :--- |
| `get_house_status` | Global Inspection | Returns the state of all lights, climate, locks, garage, and media. |
| `control_light` | Lighting | Toggles light power, brightness (0–100), and color per room. |
| `control_thermostat` | HVAC / Climate | Adjusts target temperature in Celsius and HVAC mode (`cool`, `heat`, `eco`, etc.). |
| `control_door_lock` | Entrance Security | Locks or unlocks front and back entrance doors. |
| `control_garage_door` | Access Control | Opens or closes the garage door. |
| `control_music` | Media / Audio | Controls playback, track name, and volume on living room speaker. |

---

## 2. 🌐 Complete Catalog of Alexa+ Connectable Tools

Because Alexa+ uses LLM reasoning and the open **Model Context Protocol (MCP)**, it is no longer restricted to legacy rigid schemas. **Any tool with clear parameters and natural language descriptions can be exposed to Alexa.**

### A. 🛡️ Security, Cameras & Access
* **`control_security_system(mode: str, pin: int)`**
  * *Modes*: `"home"`, `"away"`, `"night"`, `"disarmed"`
  * *Example Voice Prompt*: *"Alexa, arm the security system for the night."*
* **`get_security_camera_summary(camera_location: str)`**
  * *Locations*: `"front_porch"`, `"driveway"`, `"backyard"`
  * *Example Voice Prompt*: *"Alexa, did anyone leave a package at the front porch?"*
* **`control_alarm_siren(action: str, duration_seconds: int)`**
  * *Actions*: `"sound"`, `"silence"`
  * *Example Voice Prompt*: *"Alexa, trigger the panic alarm!"*
* **`get_window_sensors(zone: str = None)`**
  * *Example Voice Prompt*: *"Alexa, did we leave any windows open?"*

### B. 🪟 Windows, Blinds & Ventilation
* **`control_blinds(room: str, position_percent: int, tilt: int)`**
  * *Example Voice Prompt*: *"Alexa, close the bedroom blinds to 50%."*
* **`control_ceiling_fan(room: str, power: bool, speed: int, reverse: bool)`**
  * *Example Voice Prompt*: *"Alexa, turn on the living room fan to speed 3."*

### C. 🤖 Smart Appliances & Robotic Helpers
* **`control_robot_vacuum(action: str, room: str = None, mode: str = "vacuum")`**
  * *Actions*: `"start"`, `"dock"`, `"pause"`, `"spot_clean"`
  * *Example Voice Prompt*: *"Alexa, tell the robot vacuum to clean the kitchen and then dock."*
* **`control_smart_plug(device_name: str, power: bool)`**
  * *Devices*: Coffee maker, seasonal lights, space heater
  * *Example Voice Prompt*: *"Alexa, turn on the coffee maker plug."*
* **`control_oven(power: bool, target_temp_c: float, mode: str)`**
  * *Modes*: `"bake"`, `"broil"`, `"convection"`
  * *Example Voice Prompt*: *"Alexa, preheat the oven to 180 degrees Celsius."*
* **`get_appliance_status(appliance: str)`**
  * *Appliances*: `"dishwasher"`, `"washing_machine"`, `"dryer"`
  * *Example Voice Prompt*: *"Alexa, is the laundry done yet?"*

### D. 🍃 Environmental, Air Quality & Health
* **`get_air_quality(room: str = None)`**
  * Reads PM2.5, VOC, CO2 levels, and indoor humidity.
  * *Example Voice Prompt*: *"Alexa, what is the air quality in the nursery?"*
* **`control_air_purifier(room: str, power: bool, fan_speed: str)`**
  * *Speeds*: `"quiet"`, `"auto"`, `"turbo"`
  * *Example Voice Prompt*: *"Alexa, put the bedroom air purifier on quiet mode."*
* **`get_water_leak_status()`**
  * Checks flood sensors under sinks, boiler, and basement.
  * *Example Voice Prompt*: *"Alexa, are there any water leaks detected?"*

### E. 🎬 Scenes, Routines & Macro Actions
* **`activate_scene(scene_name: str)`**
  * *Presets*: `"good_morning"`, `"movie_night"`, `"bedtime"`, `"away"`, `"party"`
  * *Example Voice Prompt*: *"Alexa, let's watch a movie."* *(Dims lights to 15%, closes shades, pauses music, sets thermostat)*.
* **`set_delayed_action(tool_name: str, arguments: dict, delay_minutes: int)`**
  * *Example Voice Prompt*: *"Alexa, turn off the backyard lights in 30 minutes."*

### F. ⚡ Energy, EV & Solar
* **`get_energy_usage()`**
  * Returns real-time household Watt draw, solar generation, and battery storage.
  * *Example Voice Prompt*: *"Alexa, how much solar power are we producing right now?"*
* **`control_ev_charger(action: str, target_soc_percent: int)`**
  * *Example Voice Prompt*: *"Alexa, charge the car to 80% before tomorrow morning."*

### G. 📢 Intercom & Audio Announcements
* **`send_announcement(message: str, target_rooms: list[str])`**
  * Broadcasts text-to-speech across chosen smart speakers.
  * *Example Voice Prompt*: *"Alexa, announce that dinner is ready to all rooms."*

---

## 3. 🧠 The Core Architectural Question

> **"If Alexa understands user prompts and can interpret anything, why do we need to manually hardcode every feature like `get_house_status` or individual device tools? Is there a workaround?"**

### The Division of Labor: Brain vs. Hands
* **Alexa is the Brain**: Understands natural language, resolves ambiguity (*"it's stuffy in here"*, *"we're leaving"*), and plans which goals to achieve.
* **The MCP Server is the Hands**: Directly manipulates hardware protocols, databases, and physical states. An LLM *understands* words, but it cannot physically toggle an electrical relay or update a state dictionary without an interface.

### Why Developers Historically Hardcoded Tools
1. **Safety & Guardrails**: Prevents hallucinations (e.g. setting temperature to `1000°` or unlocking the front door when told to turn off a light).
2. **Deterministic Schemas**: Strongly-typed schemas (e.g. `brightness: 0-100`) make it easy for the LLM to provide valid arguments in one attempt.
3. **The Downside**: Heavy boilerplate. Every new gadget requires new Python methods, schema definitions, and tests.

---

## 4. 🚀 Workarounds & Modern AI Architectural Patterns

You **do not** have to hardcode individual tools. Here are the three primary alternative design patterns:

### Pattern 1: The Unified Entity Controller (2 Tools for Infinite Devices)
Instead of 50 separate tools, the MCP server exposes only **two generic meta-tools**:

```python
@mcp_server.tool(name="get_devices")
def get_devices(category: str = None) -> dict:
    """Inspect all smart devices in the house (or filter by lights, climate, security, appliances)."""
    return house.get_devices(category)

@mcp_server.tool(name="control_device")
def control_device(device_id: str, property: str, value: Any) -> str:
    """Set any property on any smart device in the house.
    Examples:
      - device_id: 'bedroom_light', property: 'brightness', value: 80
      - device_id: 'front_door', property: 'locked', value: False
      - device_id: 'robot_vacuum', property: 'action', value: 'clean'
      - device_id: 'coffee_maker', property: 'power', value: True
    """
    return house.update_device(device_id, property, value)
```

**How it works in practice:**
* User: *"Alexa, start brewing the espresso."*
* Alexa calls: `control_device(device_id="kitchen_espresso_machine", property="power", value=True)`.
* **Zero new code needed**: Alexa infers the entity and property dynamically from the house device registry.

---

### Pattern 2: MCP Resources (Eliminating `get_house_status` entirely)
The Model Context Protocol includes **Resources**—live context feeds attached directly into the AI's prompt:

```python
@mcp_server.resource("house://state")
def live_house_state() -> str:
    """Live state of all devices in the home."""
    return json.dumps(house.get_summary())
```

**Why this is revolutionary:**
* Alexa **always has the current house state in its context window before the user even speaks**.
* User: *"Alexa, why is it so cold in here?"*
* Alexa does **not** call `get_house_status`. It already reads `{climate: {current_temp_c: 16.5, mode: "off"}}` in its context and replies immediately:
  > *"The heater is currently off and the living room is at 16.5°C. Would you like me to set the thermostat to 21°C?"*

---

### Pattern 3: State-Diff / Patch Pattern (Single Macro Tool)
Used by production systems like Home Assistant and Kubernetes:

```python
@mcp_server.tool(name="apply_home_state_changes")
def apply_home_state_changes(patch: dict) -> str:
    """Applies a batch diff to device states in one atomic operation."""
    return house.apply_patch(patch)
```

**Example:**
When a user says *"Goodnight Alexa, I'm heading to sleep"*, Alexa executes one payload:
```json
{
  "lights.all": {"power": false},
  "climate.target_temperature_c": 19.5,
  "security.doors": {"locked": true},
  "security.garage_door": {"open": false},
  "media.living_room_speaker": {"playing": false}
}
```

---

## 5. ⚖️ Comparison Matrix

| Architectural Approach | Tool Count | Flexibility | Schema Safety | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Explicit Device Tools** *(Current)* | 1 per device (6+) | Low (Requires code for every new gadget) | Very High (Typed parameters) | Strict hackathons, small controlled demos |
| **Unified Controller** *(Pattern 1)* | **2 tools** | **Infinite** (Any device works automatically) | High (Dynamic validation) | **Home Assistant style setups, scalable homes** |
| **MCP Resources** *(Pattern 2)* | **0 query tools** | Real-time Context | N/A (Read-only context) | **Eliminating latency and status query calls** |
| **State Patch / Diff** *(Pattern 3)* | **1 batch tool** | High (Batch routines) | Moderate (Validates JSON patch) | Complex macro routines & multi-room scenes |
