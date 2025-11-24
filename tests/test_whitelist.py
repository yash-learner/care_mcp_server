"""Tests for whitelist manager."""

import tempfile
import os
from care_mcp_server.whitelist import WhitelistManager


def test_default_whitelist():
    """Test default whitelist contains expected operations."""
    manager = WhitelistManager()
    allowed = manager.get_allowed_operations()

    assert "api_v1_facility_create" in allowed
    assert "api_v1_facility_list" in allowed
    assert "api_v1_organization_create" in allowed
    assert "api_v1_users_list" in allowed


def test_is_allowed_for_whitelisted_operation():
    """Test is_allowed returns True for whitelisted operations."""
    manager = WhitelistManager()
    assert manager.is_allowed("api_v1_facility_create") is True
    assert manager.is_allowed("api_v1_patient_list") is True


def test_is_allowed_for_non_whitelisted_operation():
    """Test is_allowed returns False for non-whitelisted operations."""
    manager = WhitelistManager()
    assert manager.is_allowed("some_random_operation") is False


def test_is_allowed_blocks_destroy_operations():
    """Test is_allowed blocks operations with _destroy pattern."""
    manager = WhitelistManager()
    assert manager.is_allowed("api_v1_facility_destroy") is False
    assert manager.is_allowed("api_v1_patient_destroy") is False


def test_is_allowed_blocks_delete_operations():
    """Test is_allowed blocks operations with _delete pattern."""
    manager = WhitelistManager()
    assert manager.is_allowed("api_v1_facility_delete") is False
    assert manager.is_allowed("api_v1_patient_delete") is False


def test_custom_whitelist():
    """Test custom whitelist."""
    custom = ["operation_1", "operation_2"]
    manager = WhitelistManager(custom_whitelist=custom)

    assert manager.is_allowed("operation_1") is True
    assert manager.is_allowed("operation_2") is True
    assert manager.is_allowed("api_v1_facility_create") is False


def test_add_operation():
    """Test adding an operation to whitelist."""
    manager = WhitelistManager()
    manager.add_operation("new_operation")

    assert manager.is_allowed("new_operation") is True


def test_remove_operation():
    """Test removing an operation from whitelist."""
    manager = WhitelistManager()
    manager.remove_operation("api_v1_facility_create")

    assert manager.is_allowed("api_v1_facility_create") is False


def test_export_import_yaml():
    """Test exporting and importing whitelist to/from YAML."""
    manager1 = WhitelistManager()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        temp_path = f.name

    try:
        # Export
        manager1.export_to_yaml(temp_path)

        # Import
        manager2 = WhitelistManager.import_from_yaml(temp_path)

        # Verify
        assert manager1.get_allowed_operations() == manager2.get_allowed_operations()
    finally:
        os.unlink(temp_path)


def test_get_allowed_operations_returns_sorted_list():
    """Test get_allowed_operations returns a sorted list."""
    manager = WhitelistManager()
    operations = manager.get_allowed_operations()

    assert operations == sorted(operations)
