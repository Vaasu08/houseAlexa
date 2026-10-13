"""
house_state.py - The Virtual House (State Management)

Analogy for a 5yo:
This is our Lego House! It keeps track of every toy inside:
- Which lights are glowing
- How warm or cold the living room is
- Whether the front door is locked or unlocked
- What song the speaker is playing
"""

from typing import Dict, Any


class HouseState:
    def __init__(self):
        # Initial state of our house
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

        return (
            f"Thermostat set to {climate['target_temperature_c']}°C. "
            f"Current room temp is {climate['current_temperature_c']}°C (Mode: {climate['mode']})."
        )

    def set_lock(self, door: str, locked: bool) -> str:
        """Lock or unlock a door."""
        door_key = door.lower().replace(" ", "_")
        if door_key not in self.devices["security"]:
            valid_doors = ", ".join(self.devices["security"].keys())
            return f"Error: Door '{door}' not found. Available doors: {valid_doors}"

        self.devices["security"][door_key]["locked"] = locked
        status = "LOCKED" if locked else "UNLOCKED"
        return f"{door.title()} is now {status}."

    def control_media(self, action: str, track: str = None, volume: int = None) -> str:
        """Control the living room speaker (play, pause, stop, volume)."""
        speaker = self.devices["media"]["living_room_speaker"]
        action = action.lower()

        if action == "play":
            speaker["power"] = True
            speaker["playing"] = True
            if track:
                speaker["track"] = track
            return f"Playing '{speaker['track']}' at volume {speaker['volume']}%."
        elif action in ("pause", "stop"):
            speaker["playing"] = False
            return f"Music paused on living room speaker."
        elif action == "volume" and volume is not None:
            speaker["volume"] = max(0, min(100, volume))
            return f"Speaker volume set to {speaker['volume']}%."
        else:
            return f"Unknown music action '{action}'. Valid actions: play, pause, stop, volume."


# Global singleton instance of our house
house = HouseState()
