"""Tests for enhancements module."""

from care_mcp_server.enhancements import EnhancementManager, ToolEnhancement


def test_enhancement_manager_has_enhancements():
    """Test enhancement manager has enhancement data."""
    manager = EnhancementManager()
    assert len(manager.ENHANCEMENTS) > 0


def test_get_enhancement_for_existing_operation():
    """Test getting enhancement for an operation that has one."""
    manager = EnhancementManager()
    enhancement = manager.get_enhancement("api_v1_facility_create")

    assert enhancement is not None
    assert isinstance(enhancement, ToolEnhancement)
    assert "🏥" in enhancement.title
    assert "Create" in enhancement.title
    assert len(enhancement.description) > 0
    assert len(enhancement.tags) > 0
    assert len(enhancement.examples) > 0


def test_get_enhancement_for_non_existing_operation():
    """Test getting enhancement for an operation without one."""
    manager = EnhancementManager()
    enhancement = manager.get_enhancement("non_existent_operation")

    assert enhancement is None


def test_has_enhancement_true():
    """Test has_enhancement returns True for enhanced operations."""
    manager = EnhancementManager()
    assert manager.has_enhancement("api_v1_facility_create") is True
    assert manager.has_enhancement("api_v1_patient_list") is True


def test_has_enhancement_false():
    """Test has_enhancement returns False for non-enhanced operations."""
    manager = EnhancementManager()
    assert manager.has_enhancement("non_existent_operation") is False


def test_enhancement_structure():
    """Test enhancement has required structure."""
    manager = EnhancementManager()
    enhancement = manager.get_enhancement("api_v1_facility_list")

    assert hasattr(enhancement, "title")
    assert hasattr(enhancement, "description")
    assert hasattr(enhancement, "tags")
    assert hasattr(enhancement, "examples")
    assert isinstance(enhancement.tags, list)
    assert isinstance(enhancement.examples, list)


def test_all_whitelisted_operations_have_enhancements():
    """Test that key whitelisted operations have enhancements."""
    manager = EnhancementManager()

    # Check some key operations
    key_operations = [
        "api_v1_facility_create",
        "api_v1_facility_list",
        "api_v1_organization_create",
        "api_v1_users_list",
        "api_v1_patient_list",
    ]

    for op in key_operations:
        assert manager.has_enhancement(op), f"Operation {op} should have enhancement"
