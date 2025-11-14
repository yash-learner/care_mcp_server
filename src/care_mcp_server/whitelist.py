"""Whitelist management for Care API operations."""
from typing import List, Set
import yaml
from pathlib import Path


class WhitelistManager:
    """Manage allowed API operations."""
    
    # Default whitelist of allowed operations
    DEFAULT_WHITELIST = [
        # Facility operations
        "facility_create",
        "facility_list",
        "facility_retrieve",
        "facility_update",
        
        # Organization operations
        "organization_create",
        "organization_list",
        "organization_retrieve",
        
        # Location operations
        "location_create",
        "location_list",
        "location_retrieve",
        
        # Bed operations
        "bed_create",
        "bed_list",
        "bed_retrieve",
        "bed_update",
        
        # User operations
        "users_list",
        "users_retrieve",
        "users_getcurrentuser",
        
        # Geography operations
        "state_list",
        "district_list",
        "localBody_list",
        "ward_list",
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
            "blocked_patterns": self.BLOCKED_PATTERNS
        }
        
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    @classmethod
    def import_from_yaml(cls, file_path: str) -> 'WhitelistManager':
        """
        Import whitelist from YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            WhitelistManager instance with loaded whitelist
        """
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        whitelist = data.get("whitelist", cls.DEFAULT_WHITELIST)
        manager = cls(custom_whitelist=whitelist)
        
        # Update blocked patterns if provided
        if "blocked_patterns" in data:
            manager.BLOCKED_PATTERNS = data["blocked_patterns"]
        
        return manager
