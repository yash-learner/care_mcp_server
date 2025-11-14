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

    # Enhanced metadata for key operations (matching actual Care API operation IDs)
    ENHANCEMENTS: Dict[str, ToolEnhancement] = {
        "api_v1_facility_create": ToolEnhancement(
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
        "api_v1_facility_list": ToolEnhancement(
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
        "api_v1_facility_retrieve": ToolEnhancement(
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
        "api_v1_facility_update": ToolEnhancement(
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
        "api_v1_organization_create": ToolEnhancement(
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
        "api_v1_organization_list": ToolEnhancement(
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
        "api_v1_organization_retrieve": ToolEnhancement(
            title="🏢 Get Organization Details",
            description=("Retrieve detailed information about a specific organization."),
            tags=["organization", "query", "detail"],
            examples=[
                "Get details of organization ID 456",
                "Show me information about State Health Department",
            ],
        ),
        "api_v1_facility_location_create": ToolEnhancement(
            title="📍 Create Location",
            description=(
                "Create a new location within a healthcare facility. "
                "Locations represent wards, rooms, or specific areas within a facility."
            ),
            tags=["location", "setup", "create", "facility"],
            examples=[
                "Add ICU ward to facility",
                "Create emergency room location",
                "Register new isolation ward",
            ],
        ),
        "api_v1_facility_location_list": ToolEnhancement(
            title="📍 List Locations",
            description=(
                "Retrieve a list of locations within a facility. "
                "Filter by location type and availability."
            ),
            tags=["location", "query", "list", "facility"],
            examples=[
                "Show all locations in this facility",
                "List ICU wards",
                "Find available isolation rooms",
            ],
        ),
        "api_v1_facility_location_retrieve": ToolEnhancement(
            title="📍 Get Location Details",
            description=(
                "Retrieve detailed information about a specific location within a facility."
            ),
            tags=["location", "query", "detail", "facility"],
            examples=["Get details of location", "Show me information about this ward"],
        ),
        "api_v1_users_list": ToolEnhancement(
            title="👤 List Users",
            description=(
                "Retrieve a list of users in the system. "
                "Useful for user management and access control."
            ),
            tags=["user", "query", "list"],
            examples=["Show all users", "List doctors in the facility", "Find staff members"],
        ),
        "api_v1_users_retrieve": ToolEnhancement(
            title="👤 Get User Details",
            description=("Retrieve detailed information about a specific user."),
            tags=["user", "query", "detail"],
            examples=["Get user details for ID 101", "Show me Dr. Smith's information"],
        ),
        "api_v1_users_getcurrentuser_retrieve": ToolEnhancement(
            title="👤 Get Current User",
            description=("Retrieve information about the currently authenticated user."),
            tags=["user", "query", "auth"],
            examples=[
                "Who am I logged in as?",
                "Show my user information",
                "Get current user details",
            ],
        ),
        "api_v1_patient_list": ToolEnhancement(
            title="🏥 List Patients",
            description=(
                "Retrieve a list of patients in the system. "
                "Filter by facility, status, and other parameters."
            ),
            tags=["patient", "query", "list"],
            examples=[
                "Show all patients",
                "List patients in this facility",
                "Find active patients",
            ],
        ),
        "api_v1_patient_retrieve": ToolEnhancement(
            title="🏥 Get Patient Details",
            description=("Retrieve detailed information about a specific patient."),
            tags=["patient", "query", "detail"],
            examples=["Get patient details", "Show patient information"],
        ),
        "api_v1_encounter_list": ToolEnhancement(
            title="📋 List Encounters",
            description=(
                "Retrieve a list of patient encounters (visits, admissions). "
                "Encounters represent patient interactions with the healthcare system."
            ),
            tags=["encounter", "query", "list"],
            examples=["Show all encounters", "List patient visits", "Find active admissions"],
        ),
        "api_v1_encounter_retrieve": ToolEnhancement(
            title="📋 Get Encounter Details",
            description=("Retrieve detailed information about a specific patient encounter."),
            tags=["encounter", "query", "detail"],
            examples=["Get encounter details", "Show visit information"],
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
