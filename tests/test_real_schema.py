"""Tests for real Care API schema validation."""

import json
import os
from care_mcp_server.whitelist import WhitelistManager
from care_mcp_server.enhancements import EnhancementManager


def test_real_schema_exists():
    """Test that the real Care API schema file exists."""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "care_api_swagger_schema.json"
    )
    assert os.path.exists(schema_path), "care_api_swagger_schema.json should exist"


def test_whitelisted_operations_exist_in_real_schema():
    """Test that all whitelisted operations exist in the real Care API schema."""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "care_api_swagger_schema.json"
    )

    # Skip if schema doesn't exist (e.g., in CI without the file)
    if not os.path.exists(schema_path):
        return

    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Extract all operation IDs from schema
    real_operations = set()
    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            if isinstance(details, dict) and "operationId" in details:
                real_operations.add(details["operationId"])

    # Check whitelist
    manager = WhitelistManager()
    whitelist = manager.get_allowed_operations()

    missing_operations = []
    for op in whitelist:
        if op not in real_operations:
            missing_operations.append(op)

    assert (
        len(missing_operations) == 0
    ), f"Whitelisted operations not found in schema: {missing_operations}"


def test_enhanced_operations_exist_in_real_schema():
    """Test that all enhanced operations exist in the real Care API schema."""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "care_api_swagger_schema.json"
    )

    # Skip if schema doesn't exist
    if not os.path.exists(schema_path):
        return

    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Extract all operation IDs from schema
    real_operations = set()
    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            if isinstance(details, dict) and "operationId" in details:
                real_operations.add(details["operationId"])

    # Check enhancements
    manager = EnhancementManager()
    enhanced_ops = list(manager.ENHANCEMENTS.keys())

    missing_operations = []
    for op in enhanced_ops:
        if op not in real_operations:
            missing_operations.append(op)

    assert (
        len(missing_operations) == 0
    ), f"Enhanced operations not found in schema: {missing_operations}"


def test_real_schema_structure():
    """Test that the real schema has expected structure."""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "care_api_swagger_schema.json"
    )

    # Skip if schema doesn't exist
    if not os.path.exists(schema_path):
        return

    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Check basic structure
    assert "openapi" in schema, "Schema should have openapi version"
    assert "info" in schema, "Schema should have info section"
    assert "paths" in schema, "Schema should have paths section"

    # Check info
    assert "title" in schema["info"], "Schema info should have title"
    assert "version" in schema["info"], "Schema info should have version"

    # Check we have paths
    assert len(schema["paths"]) > 0, "Schema should have at least one path"


def test_real_schema_has_expected_operations():
    """Test that the real schema has expected Care API operations."""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "care_api_swagger_schema.json"
    )

    # Skip if schema doesn't exist
    if not os.path.exists(schema_path):
        return

    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Extract all operation IDs
    operations = []
    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            if isinstance(details, dict) and "operationId" in details:
                operations.append(details["operationId"])

    # Check for expected operation types
    assert any("facility" in op for op in operations), "Should have facility operations"
    assert any("organization" in op for op in operations), "Should have organization operations"
    assert any("patient" in op for op in operations), "Should have patient operations"
    assert any("users" in op for op in operations), "Should have user operations"
