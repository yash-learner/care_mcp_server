"""Whitelist management for Care API operations."""

from typing import List, Set
import yaml


class WhitelistManager:
    """Manage allowed API operations."""

    # Default whitelist of allowed operations (matching actual Care API)
    DEFAULT_WHITELIST = [
        # Facility operations
        "api_v1_facility_create",
        "api_v1_facility_list",
        "api_v1_facility_retrieve",
        "api_v1_facility_update",
        "api_v1_facility_partial_update",
        # Organization operations
        "api_v1_organization_create",
        "api_v1_organization_list",
        "api_v1_organization_retrieve",
        "api_v1_organization_update",
        "api_v1_organization_partial_update",
        # Location operations (facility-scoped)
        "api_v1_facility_location_create",
        "api_v1_facility_location_list",
        "api_v1_facility_location_retrieve",
        "api_v1_facility_location_update",
        "api_v1_facility_location_partial_update",
        # User operations
        "api_v1_users_list",
        "api_v1_users_retrieve",
        "api_v1_users_getcurrentuser_retrieve",
        "api_v1_facility_users_list",
        "api_v1_facility_users_retrieve",
        # Patient operations (read-only)
        "api_v1_patient_list",
        "api_v1_patient_retrieve",
        # Encounter operations (read-only)
        "api_v1_encounter_list",
        "api_v1_encounter_retrieve",
        # Resource operations (read-only)
        "api_v1_resource_list",
        "api_v1_resource_retrieve",
    ]

    # Patterns for blocked operations
    BLOCKED_PATTERNS = [
        "_destroy",
        "_delete",
    ]

    def __init__(self, custom_whitelist: List[str] = None):
        """
        Initialize whitelist manager.

        Args:
            custom_whitelist: Optional custom list of allowed operations
        """
        if custom_whitelist:
            self.whitelist: Set[str] = set(custom_whitelist)
        else:
            self.whitelist: Set[str] = set(self.DEFAULT_WHITELIST)

    def is_allowed(self, operation_id: str) -> bool:
        """
        Check if an operation is allowed.

        Args:
            operation_id: The operation ID to check

        Returns:
            True if allowed, False otherwise
        """
        # Check if operation matches any blocked pattern
        for pattern in self.BLOCKED_PATTERNS:
            if pattern in operation_id:
                return False

        # Check if operation is in whitelist
        return operation_id in self.whitelist

    def get_allowed_operations(self) -> List[str]:
        """
        Get list of all allowed operations.

        Returns:
            List of allowed operation IDs
        """
        return sorted(list(self.whitelist))

    def add_operation(self, operation_id: str) -> None:
        """
        Add an operation to the whitelist.

        Args:
            operation_id: The operation ID to add
        """
        self.whitelist.add(operation_id)

    def remove_operation(self, operation_id: str) -> None:
        """
        Remove an operation from the whitelist.

        Args:
            operation_id: The operation ID to remove
        """
        self.whitelist.discard(operation_id)

    def export_to_yaml(self, file_path: str) -> None:
        """
        Export whitelist to YAML file.

        Args:
            file_path: Path to save the YAML file
        """
        data = {
            "whitelist": self.get_allowed_operations(),
            "blocked_patterns": self.BLOCKED_PATTERNS,
        }

        with open(file_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    @classmethod
    def import_from_yaml(cls, file_path: str) -> "WhitelistManager":
        """
        Import whitelist from YAML file.

        Args:
            file_path: Path to the YAML file

        Returns:
            WhitelistManager instance with loaded whitelist
        """
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        whitelist = data.get("whitelist", cls.DEFAULT_WHITELIST)
        manager = cls(custom_whitelist=whitelist)

        # Update blocked patterns if provided
        if "blocked_patterns" in data:
            manager.BLOCKED_PATTERNS = data["blocked_patterns"]

        return manager
