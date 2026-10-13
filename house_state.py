"""
house_state.py - The Virtual House (State Management)

Analogy for a 5yo:
This is our Lego House! It keeps track of every toy inside:
- Which lights are glowing
- How warm or cold the living room is
- Whether the front door is locked or unlocked
- What song the speaker is playing
"""

import json
import os
from typing import Dict, Any


class HouseState:
    def __init__(self, storage_file: str = "house_state.json"):
        self.storage_file = storage_file
        # Initial default state of our house
        self.devices: Dict[str, Any] = {
            "lights": {
                "living_room": {"power": False, "brightness": 100, "color": "warm_white"},
                "bedroom": {"power": False, "brightness": 70, "color": "soft_white"},
                "kitchen": {"power": False, "brightness": 100, "color": "daylight"},
            },
            "climate": {
                "current_temperature_c": 22.0,
                "target_temperature_c": 22.0,
                "mode": "off",  # "off", "cool", "heat", "fan", "eco"
            },
            "security": {
                "front_door": {"locked": True},
                "back_door": {"locked": True},
                "garage_door": {"open": False},
            },
            "media": {
                "living_room_speaker": {
                    "power": False,
                    "volume": 35,
                    "playing": False,
                    "track": "None",
                }
            },
        }

        # Load persisted state from disk if file exists, or save defaults
        if not self.load_from_disk():
            self.save_to_disk()

    def save_to_disk(self, filepath: str = None) -> None:
        """Persists current state to a JSON file."""
        path = filepath or self.storage_file
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.devices, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save house state to {path}: {e}")

    def load_from_disk(self, filepath: str = None) -> bool:
        """Loads state from disk if present."""
        path = filepath or self.storage_file
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "lights" in data and "climate" in data:
                        self.devices = data
                        return True
            except Exception as e:
                print(f"Warning: Failed to load house state from {path}: {e}")
        return False

    def get_summary(self) -> Dict[str, Any]:
        """Returns the full status of all items in the house."""
        return self.devices

    def set_light(self, room: str, power: bool, brightness: int = None, color: str = None) -> str:
        """Turn a light on or off, and optionally set brightness and color."""
        room_key = room.lower().replace(" ", "_")
        if room_key not in self.devices["lights"]:
            valid_rooms = ", ".join(self.devices["lights"].keys())
            return f"Error: Room '{room}' not found. Available rooms: {valid_rooms}"

        light = self.devices["lights"][room_key]
        light["power"] = power
        if brightness is not None:
            light["brightness"] = max(0, min(100, brightness))
        if color is not None:
            light["color"] = color

        self.save_to_disk()
        status = "ON" if power else "OFF"
        return f"{room.title()} light is now {status} (brightness: {light['brightness']}%, color: {light['color']})."

    def set_thermostat(self, target_c: float, mode: str = None) -> str:
        """Set the target temperature and optional mode (cool/heat/eco/off)."""
        climate = self.devices["climate"]
        climate["target_temperature_c"] = round(target_c, 1)
        if mode:
            valid_modes = ["off", "cool", "heat", "fan", "eco"]
            if mode.lower() in valid_modes:
                climate["mode"] = mode.lower()

        self.save_to_disk()
        return (
            f"Thermostat set to {climate['target_temperature_c']}°C. "
            f"Current room temp is {climate['current_temperature_c']}°C (Mode: {climate['mode']})."
        )

    def set_lock(self, door: str, locked: bool) -> str:
        """Lock or unlock an entrance door (front_door, back_door)."""
        door_key = door.lower().replace(" ", "_")
        valid_doors = [k for k, v in self.devices["security"].items() if "locked" in v]
        if door_key not in valid_doors:
            doors_str = ", ".join(valid_doors)
            return f"Error: Door '{door}' not found. Available lockable doors: {doors_str}. (For garage door, use set_garage_door)"

        self.devices["security"][door_key]["locked"] = locked
        self.save_to_disk()
        status = "LOCKED" if locked else "UNLOCKED"
        return f"{door.title()} is now {status}."

    def set_garage_door(self, open: bool) -> str:
        """Open or close the garage door."""
        if "garage_door" not in self.devices["security"]:
            return "Error: Garage door device not found in security system."

        self.devices["security"]["garage_door"]["open"] = open
        self.save_to_disk()
        status = "OPEN" if open else "CLOSED"
        return f"Garage door is now {status}."

    def control_media(self, action: str, track: str = None, volume: int = None) -> str:
        """Control the living room speaker (play, pause, stop, volume)."""
        speaker = self.devices["media"]["living_room_speaker"]
        action = action.lower()

        if action == "play":
            speaker["power"] = True
            speaker["playing"] = True
            if track:
                speaker["track"] = track
            self.save_to_disk()
            return f"Playing '{speaker['track']}' at volume {speaker['volume']}%."
        elif action in ("pause", "stop"):
            speaker["playing"] = False
            self.save_to_disk()
            return f"Music paused on living room speaker."
        elif action == "volume" and volume is not None:
            speaker["volume"] = max(0, min(100, volume))
            self.save_to_disk()
            return f"Speaker volume set to {speaker['volume']}%."
        else:
            return f"Unknown music action '{action}'. Valid actions: play, pause, stop, volume."


# Global singleton instance of our house
house = HouseState()

