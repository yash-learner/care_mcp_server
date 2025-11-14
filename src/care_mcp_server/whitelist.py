"""
API operation whitelist for Care MCP Server
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


# Default whitelist (focused on setup operations)
DEFAULT_WHITELIST: Dict[str, bool] = {
    # Facility/Hospital Management
    "facility_create": True,
    "facility_list": True,
    "facility_retrieve": True,
    "facility_update": True,
    "facility_partial_update": True,

    # Organization Management
    "organization_create": True,
    "organization_list": True,
    "organization_retrieve": True,
    "organization_update": True,

    # Location Management
    "location_create": True,
    "location_list": True,
    "location_retrieve": True,
    "location_update": True,

    # Asset Location
    "assetlocation_create": True,
    "assetlocation_list": True,
    "assetlocation_retrieve": True,

    # Bed Management
    "bed_create": True,
    "bed_list": True,
    "bed_retrieve": True,
    "bed_update": True,

    # User Management
    "users_list": True,
    "users_retrieve": True,
    "users_getcurrentuser": True,

    # Geographic Data
    "state_list": True,
    "district_list": True,
    "localBody_list": True,
    "ward_list": True,

    # SAFETY: Explicitly disabled operations
    "facility_destroy": False,
    "organization_destroy": False,
    "patient_destroy": False,
    "consultation_destroy": False,
    "user_destroy": False,
}


class WhitelistManager:
    """Manage API operation whitelist"""

    def __init__(self, whitelist: Optional[Dict[str, bool]] = None):
        self.whitelist = whitelist or DEFAULT_WHITELIST.copy()

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "WhitelistManager":
        """Load whitelist from YAML file"""

        if yaml is None:  # pragma: no cover - optional dependency guard
            raise RuntimeError("PyYAML is required to load YAML whitelist files")

        with open(yaml_path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}

        return cls(whitelist=data.get("whitelist", DEFAULT_WHITELIST))

    def is_allowed(self, operation_id: str) -> bool:
        """Check if an operation is whitelisted"""
        return self.whitelist.get(operation_id, False)

    def add_operation(self, operation_id: str, allowed: bool = True) -> None:
        """Add or update an operation in the whitelist"""
        self.whitelist[operation_id] = allowed

    def remove_operation(self, operation_id: str) -> None:
        """Remove an operation from whitelist"""
        self.whitelist.pop(operation_id, None)

    def get_allowed_operations(self) -> List[str]:
        """Get list of all allowed operation IDs"""
        return [op for op, allowed in self.whitelist.items() if allowed]

    def export_yaml(self, output_path: Path) -> None:
        """Export whitelist to YAML file"""

        if yaml is None:  # pragma: no cover - optional dependency guard
            raise RuntimeError("PyYAML is required to export YAML whitelist files")

        with open(output_path, "w", encoding="utf-8") as handle:
            yaml.dump({"whitelist": self.whitelist}, handle, default_flow_style=False)
