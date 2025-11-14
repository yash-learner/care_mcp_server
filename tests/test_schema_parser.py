"""Tests for schema parser module."""

from care_mcp_server.schema_parser import SchemaParser


def test_schema_parser_initialization():
    """Test schema parser initializes correctly."""
    parser = SchemaParser("https://example.com/schema/")
    assert parser.schema_url == "https://example.com/schema/"
    assert parser.schema is None
    assert parser.paths == {}
    assert parser.components == {}


def test_get_param_type_mapping():
    """Test OpenAPI to Python type mapping."""
    parser = SchemaParser("https://example.com/schema/")

    assert parser._get_param_type({"type": "string"}) == "str"
    assert parser._get_param_type({"type": "integer"}) == "int"
    assert parser._get_param_type({"type": "number"}) == "float"
    assert parser._get_param_type({"type": "boolean"}) == "bool"
    assert parser._get_param_type({"type": "array"}) == "list"
    assert parser._get_param_type({"type": "object"}) == "dict"
    assert parser._get_param_type({}) == "string"


def test_resolve_ref():
    """Test $ref resolution."""
    parser = SchemaParser("https://example.com/schema/")
    parser.schema = {
        "components": {
            "schemas": {"TestModel": {"type": "object", "properties": {"id": {"type": "integer"}}}}
        }
    }

    resolved = parser._resolve_ref("#/components/schemas/TestModel")
    assert resolved["type"] == "object"
    assert "properties" in resolved


def test_resolve_invalid_ref():
    """Test resolving an invalid $ref returns empty dict."""
    parser = SchemaParser("https://example.com/schema/")
    parser.schema = {"components": {}}

    resolved = parser._resolve_ref("#/components/schemas/NonExistent")
    assert resolved == {}


def test_extract_properties():
    """Test extracting properties from schema."""
    parser = SchemaParser("https://example.com/schema/")

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Name field"},
            "age": {"type": "integer", "description": "Age field"},
        },
        "required": ["name"],
    }

    properties = parser._extract_properties(schema)

    assert "name" in properties
    assert "age" in properties
    assert properties["name"]["type"] == "str"
    assert properties["name"]["required"] is True
    assert properties["age"]["type"] == "int"
    assert properties["age"]["required"] is False


def test_get_operations_with_empty_schema():
    """Test get_operations returns empty list when no schema loaded."""
    parser = SchemaParser("https://example.com/schema/")
    operations = parser.get_operations()
    assert operations == []


def test_get_operations_with_mock_schema():
    """Test get_operations extracts operations correctly."""
    parser = SchemaParser("https://example.com/schema/")
    parser.schema = {}
    parser.paths = {
        "/api/v1/facility/": {
            "get": {
                "operationId": "facility_list",
                "summary": "List facilities",
                "parameters": [],
                "responses": {},
            },
            "post": {
                "operationId": "facility_create",
                "summary": "Create facility",
                "parameters": [],
                "responses": {},
            },
        }
    }

    operations = parser.get_operations()

    assert len(operations) == 2
    operation_ids = [op["operation_id"] for op in operations]
    assert "facility_list" in operation_ids
    assert "facility_create" in operation_ids


def test_get_operation_by_id():
    """Test getting a specific operation by ID."""
    parser = SchemaParser("https://example.com/schema/")
    parser.schema = {}
    parser.paths = {
        "/api/v1/facility/": {
            "get": {
                "operationId": "facility_list",
                "summary": "List facilities",
                "parameters": [],
                "responses": {},
            }
        }
    }

    operation = parser.get_operation_by_id("facility_list")
    assert operation is not None
    assert operation["operation_id"] == "facility_list"

    non_existent = parser.get_operation_by_id("non_existent")
    assert non_existent is None
