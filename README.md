# 🏠 houseAlexa MCP Server

A self-hosted **Model Context Protocol (MCP)** server built in Python for **Alexa+** integrations and local AI testing.

Complies directly with the Amazon Developer Hackathon specification:
> *"Build a self-hosted MCP server (spec 2025-11-25 or later, Streamable HTTP) or an Agent Skill. MCP is the open standard that powers Alexa+ integrations."*

---

## 🧸 How It Works (In Plain English)

1. **The Dollhouse (`house_state.py`)**: Keeps track of virtual lights, thermostats, locks, and speakers.
2. **The Base Station (`server.py`)**: The MCP server that exposes tools via **Streamable HTTP** (`/mcp` endpoint) on port `8000`.
3. **The Tester (`test_client.py`)**: Connects over Streamable HTTP, lists all tools, and tests each action.

---

## 🚀 Quickstart

### 1. Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Start the MCP Server
```powershell
python server.py --host 127.0.0.1 --port 8000 --path /mcp
```
The server will start listening at:
`http://127.0.0.1:8000/mcp`

### 3. Run the Automated Tests (In another terminal)
```powershell
python test_client.py
```

---

## 🛠️ Available Smart Home Tools

| Tool Name | What It Does | Example Arguments |
| :--- | :--- | :--- |
| `get_house_status` | Returns the status of all devices in the home. | None |
| `control_light` | Controls light power, brightness, and color. | `{"room": "bedroom", "power": true, "brightness": 85}` |
| `control_thermostat` | Sets target AC/heating temperature & HVAC mode. | `{"temperature_celsius": 21.0, "mode": "cool"}` |
| `control_door_lock` | Locks or unlocks entrance doors. | `{"door": "front_door", "locked": true}` |
| `control_music` | Controls music playback & volume on speaker. | `{"action": "play", "track": "Lo-Fi Beats", "volume": 60}` |

---

## 🌐 Connecting to Alexa+ (When Ready)

To allow Amazon's Alexa+ to reach your self-hosted MCP server:

1. Expose your local port `8000` via a secure tunnel (e.g., [ngrok](https://ngrok.com/)):
   ```bash
   ngrok http 8000
   ```
2. Copy the public HTTPS forwarding URL:
   `https://<your-id>.ngrok-free.app/mcp`
3. Provide this URL to your Alexa+ add-on / hackathon submission.
