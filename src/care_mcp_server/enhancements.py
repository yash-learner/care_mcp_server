"""
Tool metadata enhancements for better AI context
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


@dataclass
class ToolEnhancement:
    """Enhanced metadata for an MCP tool."""

    operation_id: str
    title: str
    description: str
    tags: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)


# Default enhancements
DEFAULT_ENHANCEMENTS: Dict[str, ToolEnhancement] = {
    "facility_create": ToolEnhancement(
        operation_id="facility_create",
        title="🏥 Create Healthcare Facility",
        description="""Create a new hospital, clinic, or healthcare facility.

This is the first step in setting up a new healthcare location. Required information:
- Facility name
- Facility type (Hospital, Clinic, Primary Health Center, etc.)
- Address and location details
- Contact information
- Administrative details

Use this to onboard new hospitals, clinics, COVID care centers, or primary health centers.""",
        tags=["setup", "hospital", "onboarding", "facility"],
        examples=[
            "Create a new district hospital in Kerala",
            "Set up a COVID care center in Mumbai",
            "Register a primary health center",
        ],
    ),
    "organization_create": ToolEnhancement(
        operation_id="organization_create",
        title="🏢 Create Healthcare Organization",
        description="""Create a healthcare organization (hospital network, health department, NGO).

Organizations manage groups of facilities and administrative hierarchies. Examples:
- State/District health departments
- Hospital chains or networks
- NGOs running healthcare facilities
- Medical colleges with teaching hospitals""",
        tags=["setup", "organization", "onboarding"],
        examples=[
            "Create a state health department organization",
            "Set up a hospital chain network",
            "Register an NGO healthcare organization",
        ],
    ),
    "location_create": ToolEnhancement(
        operation_id="location_create",
        title="📍 Create Location Within Facility",
        description="""Create specific locations within a healthcare facility.

Locations organize the physical layout: wards, rooms, departments, buildings.
This helps with patient tracking, bed management, and resource allocation.""",
        tags=["setup", "location", "facility-management"],
        examples=[
            "Add ICU ward to a hospital",
            "Create OPD consultation rooms",
            "Set up pharmacy location",
        ],
    ),
    "bed_create": ToolEnhancement(
        operation_id="bed_create",
        title="🛏️ Create and Register Beds",
        description="""Register beds within a facility for patient and capacity management.

Track bed availability, occupancy status, and allocate beds to patients.
Essential for managing facility capacity and patient admissions.""",
        tags=["setup", "bed-management", "capacity"],
        examples=[
            "Add 10 ICU beds to the facility",
            "Register 50 general ward beds",
            "Set up 5 isolation beds",
        ],
    ),
}


class EnhancementManager:
    """Manage tool enhancements."""

    def __init__(self, enhancements: Optional[Dict[str, ToolEnhancement]] = None):
        self.enhancements = enhancements or DEFAULT_ENHANCEMENTS.copy()

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "EnhancementManager":
        """Load enhancements from YAML file."""

        if yaml is None:  # pragma: no cover - optional dependency guard
            raise RuntimeError("PyYAML is required to load YAML enhancement files")

        with open(yaml_path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}

        enhancements: Dict[str, ToolEnhancement] = {}
        for item in data.get("enhancements", []):
            enhancement = ToolEnhancement(**item)
            enhancements[enhancement.operation_id] = enhancement

        return cls(enhancements=enhancements)

    def get_enhancement(self, operation_id: str) -> Optional[ToolEnhancement]:
        """Get enhancement for an operation."""

        return self.enhancements.get(operation_id)

    def add_enhancement(self, enhancement: ToolEnhancement) -> None:
        """Add or update an enhancement."""

        self.enhancements[enhancement.operation_id] = enhancement

    def export_yaml(self, output_path: Path) -> None:
        """Export enhancements to YAML."""

        if yaml is None:  # pragma: no cover - optional dependency guard
            raise RuntimeError("PyYAML is required to export YAML enhancement files")

        data = {
            "enhancements": [
                asdict(enhancement) for enhancement in self.enhancements.values()
            ]
        }

        with open(output_path, "w", encoding="utf-8") as handle:
            yaml.dump(data, handle, default_flow_style=False)
