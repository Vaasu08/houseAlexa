"""
house_state.py - The Virtual House (Dynamic Entity Registry & State Manager)

Analogy for a 5yo:
This is our Universal Toy Box!
Instead of a separate rigid cubby for every toy, each toy has its own tag:
- living_room_light, front_door, robot_vacuum, coffee_maker...
You can check on any toy or change any property on the fly without needing
a new tool for every gadget!
"""

import json
import os
from typing import Dict, Any, Optional


class HouseState:
    DEFAULT_DEVICES: Dict[str, Dict[str, Any]] = {
        "living_room_light": {
            "category": "lighting",
            "room": "living_room",
            "power": False,
            "brightness": 100,
            "color": "warm_white",
        },
        "bedroom_light": {
            "category": "lighting",
            "room": "bedroom",
            "power": False,
            "brightness": 70,
            "color": "soft_white",
        },
        "kitchen_light": {
            "category": "lighting",
            "room": "kitchen",
            "power": False,
            "brightness": 100,
            "color": "daylight",
        },
        "thermostat": {
            "category": "climate",
            "room": "house",
            "current_temperature_c": 22.0,
            "target_temperature_c": 22.0,
            "mode": "off",
        },
        "front_door": {
            "category": "security",
            "room": "entrance",
            "locked": True,
        },
        "back_door": {
            "category": "security",
            "room": "backyard",
            "locked": True,
        },
        "garage_door": {
            "category": "security",
            "room": "garage",
            "open": False,
        },
        "living_room_speaker": {
            "category": "media",
            "room": "living_room",
            "power": False,
            "volume": 35,
            "playing": False,
            "track": "None",
        },
    }

    BUILTIN_SCENES: Dict[str, Dict[str, Dict[str, Any]]] = {
        "bedtime": {
            "living_room_light": {"power": False},
            "kitchen_light": {"power": False},
            "bedroom_light": {"power": True, "brightness": 15, "color": "warm_amber"},
            "front_door": {"locked": True},
            "back_door": {"locked": True},
            "garage_door": {"open": False},
            "thermostat": {"target_temperature_c": 19.5, "mode": "cool"},
            "living_room_speaker": {"playing": False},
        },
        "leaving_home": {
            "living_room_light": {"power": False},
            "bedroom_light": {"power": False},
            "kitchen_light": {"power": False},
            "front_door": {"locked": True},
            "back_door": {"locked": True},
            "garage_door": {"open": False},
            "thermostat": {"mode": "eco"},
            "living_room_speaker": {"playing": False},
        },
        "movie_night": {
            "living_room_light": {"power": True, "brightness": 20, "color": "deep_blue"},
            "kitchen_light": {"power": False},
            "bedroom_light": {"power": False},
            "thermostat": {"target_temperature_c": 21.0, "mode": "cool"},
            "living_room_speaker": {"power": True, "volume": 50, "playing": False},
        },
        "good_morning": {
            "bedroom_light": {"power": True, "brightness": 80, "color": "daylight"},
            "kitchen_light": {"power": True, "brightness": 100, "color": "daylight"},
            "front_door": {"locked": True},
            "thermostat": {"target_temperature_c": 22.0, "mode": "cool"},
        },
    }

    def __init__(self, storage_file: str = "house_state.json"):
        self.storage_file = storage_file
        self.devices: Dict[str, Dict[str, Any]] = dict(self.DEFAULT_DEVICES)

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
        """Loads state from disk if present, migrating legacy nested schema if found."""
        path = filepath or self.storage_file
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        # Detect and migrate legacy schema if needed
                        if "lights" in data and "climate" in data:
                            migrated = dict(self.DEFAULT_DEVICES)
                            for room, light in data.get("lights", {}).items():
                                migrated[f"{room}_light"] = {"category": "lighting", "room": room, **light}
                            if "climate" in data:
                                migrated["thermostat"] = {"category": "climate", "room": "house", **data["climate"]}
                            for d_key, sec in data.get("security", {}).items():
                                migrated[d_key] = {"category": "security", **sec}
                            if "media" in data and "living_room_speaker" in data["media"]:
                                migrated["living_room_speaker"] = {"category": "media", **data["media"]["living_room_speaker"]}
                            self.devices = migrated
                            self.save_to_disk()
                            return True
                        else:
                            self.devices = data
                            return True
            except Exception as e:
                print(f"Warning: Failed to load house state from {path}: {e}")
        return False

    def get_summary(self) -> Dict[str, Any]:
        """Returns the full status of all items in the house."""
        return self.devices

    def get_devices(self, filter_query: Optional[str] = None) -> Dict[str, Any]:
        """Filter devices by device_id, category, or room. Returns all if None."""
        if not filter_query:
            return self.devices

        q = filter_query.lower().strip()
        matched = {}
        for dev_id, dev_props in self.devices.items():
            category = dev_props.get("category", "").lower()
            room = dev_props.get("room", "").lower()
            if q in dev_id.lower() or q in category or q in room:
                matched[dev_id] = dev_props

        return matched if matched else self.devices

    def update_device(self, device_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamically update any property on any device. Auto-registers new devices."""
        dev_key = device_id.lower().replace(" ", "_").strip()

        if dev_key not in self.devices:
            # Dynamically register new device on the fly!
            self.devices[dev_key] = {
                "category": updates.get("category", "appliance"),
                "room": updates.get("room", "general"),
            }

        # Apply updates
        for prop, val in updates.items():
            self.devices[dev_key][prop] = val

        self.save_to_disk()
        return {
            "device_id": dev_key,
            "status": "updated",
            "current_state": self.devices[dev_key],
        }

    def batch_update(self, updates_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Apply state changes to multiple devices at once."""
        results = {}
        for dev_id, updates in updates_map.items():
            res = self.update_device(dev_id, updates)
            results[dev_id] = res["current_state"]
        return {"status": "success", "updated_devices": results}

    def activate_scene(self, scene_name: str) -> Dict[str, Any]:
        """Activates a predefined multi-device scene or returns available scenes."""
        scene_key = scene_name.lower().replace(" ", "_").strip()
        if scene_key not in self.BUILTIN_SCENES:
            available = ", ".join(self.BUILTIN_SCENES.keys())
            return {
                "status": "error",
                "message": f"Scene '{scene_name}' not found. Available scenes: {available}",
            }

        scene_updates = self.BUILTIN_SCENES[scene_key]
        self.batch_update(scene_updates)
        return {
            "status": "active",
            "scene": scene_key,
            "applied_changes": scene_updates,
        }


# Global singleton instance of our house
house = HouseState()
