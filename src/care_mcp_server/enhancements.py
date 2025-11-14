"""AI-friendly metadata enhancements for Care API operations."""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ToolEnhancement:
    """Enhancement metadata for a tool."""

    title: str
    description: str
    tags: List[str]
    examples: List[str]


class EnhancementManager:
    """Manage AI-friendly enhancements for API operations."""

    # Enhanced metadata for key operations
    ENHANCEMENTS: Dict[str, ToolEnhancement] = {
        "facility_create": ToolEnhancement(
            title="🏥 Create Healthcare Facility",
            description=(
                "Create a new healthcare facility in the Care system. "
                "This includes hospitals, clinics, COVID care centers, and other medical institutions. "
                "Provide details like facility name, type, address, and contact information."
            ),
            tags=["facility", "setup", "create", "healthcare"],
            examples=[
                "Create a new hospital named 'City General Hospital'",
                "Add a COVID care center in downtown",
                "Register a new clinic facility",
            ],
        ),
        "facility_list": ToolEnhancement(
            title="🏥 List Healthcare Facilities",
            description=(
                "Retrieve a list of healthcare facilities registered in the system. "
                "You can filter by state, district, facility type, and other parameters. "
                "Useful for finding available facilities in a specific location."
            ),
            tags=["facility", "query", "list", "healthcare"],
            examples=[
                "Show me all hospitals in Maharashtra",
                "List COVID care centers in Kerala",
                "Find all facilities in Mumbai district",
            ],
        ),
        "facility_retrieve": ToolEnhancement(
            title="🏥 Get Facility Details",
            description=(
                "Retrieve detailed information about a specific healthcare facility. "
                "Provides complete facility data including address, contact, capacity, and features."
            ),
            tags=["facility", "query", "detail", "healthcare"],
            examples=[
                "Get details of facility ID 123",
                "Show me information about City General Hospital",
                "What are the details of this facility?",
            ],
        ),
        "facility_update": ToolEnhancement(
            title="🏥 Update Facility Information",
            description=(
                "Update information for an existing healthcare facility. "
                "You can modify facility details like name, address, contact info, capacity, and features."
            ),
            tags=["facility", "update", "modify", "healthcare"],
            examples=[
                "Update the phone number for facility ID 123",
                "Change the capacity of City General Hospital",
                "Modify facility address",
            ],
        ),
        "organization_create": ToolEnhancement(
            title="🏢 Create Organization",
            description=(
                "Create a new organization in the Care system. "
                "Organizations can represent health departments, NGOs, or other entities "
                "managing multiple facilities."
            ),
            tags=["organization", "setup", "create"],
            examples=[
                "Create a new health department organization",
                "Register an NGO organization",
                "Add a new organization for managing facilities",
            ],
        ),
        "organization_list": ToolEnhancement(
            title="🏢 List Organizations",
            description=(
                "Retrieve a list of organizations in the system. "
                "Organizations manage and coordinate healthcare facilities."
            ),
            tags=["organization", "query", "list"],
            examples=[
                "Show me all organizations",
                "List health department organizations",
                "Find organizations in this state",
            ],
        ),
        "organization_retrieve": ToolEnhancement(
            title="🏢 Get Organization Details",
            description=("Retrieve detailed information about a specific organization."),
            tags=["organization", "query", "detail"],
            examples=[
                "Get details of organization ID 456",
                "Show me information about State Health Department",
            ],
        ),
        "bed_create": ToolEnhancement(
            title="🛏️ Create Bed",
            description=(
                "Create a new bed resource in a facility. "
                "Specify bed type (ICU, HDU, oxygen, etc.) and associated facility."
            ),
            tags=["bed", "setup", "create", "capacity"],
            examples=[
                "Add 10 ICU beds to facility",
                "Create oxygen beds in this hospital",
                "Register new HDU beds",
            ],
        ),
        "bed_list": ToolEnhancement(
            title="🛏️ List Beds",
            description=(
                "Retrieve a list of beds with their availability status. "
                "Filter by facility, bed type, and availability."
            ),
            tags=["bed", "query", "list", "capacity"],
            examples=[
                "Show available ICU beds",
                "List all beds in this facility",
                "Find oxygen beds in the district",
            ],
        ),
        "bed_retrieve": ToolEnhancement(
            title="🛏️ Get Bed Details",
            description=("Retrieve detailed information about a specific bed resource."),
            tags=["bed", "query", "detail", "capacity"],
            examples=["Get details of bed ID 789", "Show me information about this bed"],
        ),
        "bed_update": ToolEnhancement(
            title="🛏️ Update Bed Information",
            description=("Update bed information including availability status and metadata."),
            tags=["bed", "update", "modify", "capacity"],
            examples=["Update bed availability", "Mark bed as occupied", "Change bed type"],
        ),
        "users_list": ToolEnhancement(
            title="👤 List Users",
            description=(
                "Retrieve a list of users in the system. "
                "Useful for user management and access control."
            ),
            tags=["user", "query", "list"],
            examples=["Show all users", "List doctors in the facility", "Find staff members"],
        ),
        "users_retrieve": ToolEnhancement(
            title="👤 Get User Details",
            description=("Retrieve detailed information about a specific user."),
            tags=["user", "query", "detail"],
            examples=["Get user details for ID 101", "Show me Dr. Smith's information"],
        ),
        "users_getcurrentuser": ToolEnhancement(
            title="👤 Get Current User",
            description=("Retrieve information about the currently authenticated user."),
            tags=["user", "query", "auth"],
            examples=[
                "Who am I logged in as?",
                "Show my user information",
                "Get current user details",
            ],
        ),
        "state_list": ToolEnhancement(
            title="🗺️ List States",
            description=(
                "Retrieve a list of states/provinces in the system. "
                "Useful for geographic filtering and organization."
            ),
            tags=["geography", "query", "list"],
            examples=["List all states", "Show available states", "What states are in the system?"],
        ),
        "district_list": ToolEnhancement(
            title="🗺️ List Districts",
            description=(
                "Retrieve a list of districts within a state. " "Helps with location-based queries."
            ),
            tags=["geography", "query", "list"],
            examples=[
                "List districts in Maharashtra",
                "Show all districts",
                "What districts are available?",
            ],
        ),
        "localBody_list": ToolEnhancement(
            title="🗺️ List Local Bodies",
            description=(
                "Retrieve a list of local bodies (municipalities, corporations) within a district."
            ),
            tags=["geography", "query", "list"],
            examples=[
                "List local bodies in this district",
                "Show municipalities",
                "What local bodies are available?",
            ],
        ),
        "ward_list": ToolEnhancement(
            title="🗺️ List Wards",
            description=(
                "Retrieve a list of wards within a local body. "
                "Most granular level of geographic organization."
            ),
            tags=["geography", "query", "list"],
            examples=[
                "List wards in this local body",
                "Show all wards",
                "What wards are available?",
            ],
        ),
    }

    def get_enhancement(self, operation_id: str) -> Optional[ToolEnhancement]:
        """
        Get enhancement metadata for an operation.

        Args:
            operation_id: The operation ID to get enhancement for

        Returns:
            ToolEnhancement or None if not found
        """
        return self.ENHANCEMENTS.get(operation_id)

    def has_enhancement(self, operation_id: str) -> bool:
        """
        Check if an operation has enhancement metadata.

        Args:
            operation_id: The operation ID to check

        Returns:
            True if enhancement exists, False otherwise
        """
        return operation_id in self.ENHANCEMENTS
