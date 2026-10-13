# 🏠 houseAlexa MCP Server (v2.0 AI-First Dynamic Architecture)

A self-hosted **Model Context Protocol (MCP)** server built in Python for **Alexa+** integrations and generative AI agents.

Complies directly with the Amazon Developer Hackathon specification:
> *"Build a self-hosted MCP server (spec 2025-11-25 or later, Streamable HTTP) or an Agent Skill. MCP is the open standard that powers Alexa+ integrations."*

---

## 🧠 Why AI-First Dynamic Architecture?

In traditional legacy smart homes, developers had to hardcode a separate API endpoint for every single gadget (lights, plugs, locks, vacuums).

**houseAlexa v2.0 is built for Generative AI**:
1. **Dynamic Entity Registry (`house_state.py`)**: Can control any device or auto-register brand new appliances on the fly (e.g., `robot_vacuum`, `coffee_maker`, `sprinklers`) with **zero Python code changes**.
2. **Dynamic Tools (`server.py`)**: Rather than 20 repetitive functions, it exposes 3 powerful meta-tools (`control_device`, `get_devices`, `apply_scene`) and a live MCP prompt resource (`house://devices`).
3. **Automated State Persistence**: Device state is automatically saved to `house_state.json` and restored on reboot.

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

## 🛠️ Dynamic MCP Tools & Resources

### Live MCP Resource
* **`house://devices`**: Live context stream providing real-time device states directly into Alexa+'s prompt context window before speech interaction.

### Dynamic Tools
| Tool Name | What It Does | Example Arguments |
| :--- | :--- | :--- |
| `get_devices` | Inspects all devices, or filters by category or room. | `{"filter": "lighting"}` or `{"filter": "bedroom"}` |
| `control_device` | Dynamically updates any property on any existing or newly added device. | `{"device_id": "robot_vacuum", "updates": {"status": "cleaning_kitchen", "battery": 90}}` |
| `apply_scene` | Activates pre-set scenes (`bedtime`, `movie_night`, `leaving_home`, `good_morning`) or batch updates. | `{"scene_name": "movie_night"}` |

> 💾 **State Persistence**: Device states automatically persist to `house_state.json` on any change and reload when the server starts.

---

## 🌐 Connecting to Alexa+ (When Ready)

1. Expose your local port `8000` via a secure tunnel (e.g., [ngrok](https://ngrok.com/)):
   ```bash
   ngrok http 8000
   ```
2. Copy the public HTTPS forwarding URL:
   `https://<your-id>.ngrok-free.app/mcp`
3. Provide this URL to your Alexa+ add-on manifest using `@alexa-ai/cli`.
