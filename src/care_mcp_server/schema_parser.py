"""OpenAPI schema parser for Care API."""

from typing import Dict, List, Any, Optional
import httpx
import yaml


class SchemaParser:
    """Parse OpenAPI schema from Care API."""

    def __init__(self, schema_url: str):
        """Initialize schema parser with schema URL."""
        self.schema_url = schema_url
        self.schema: Optional[Dict[str, Any]] = None
        self.paths: Dict[str, Any] = {}
        self.components: Dict[str, Any] = {}

    async def fetch_schema(self) -> bool:
        """
        Fetch OpenAPI schema from URL.

        Returns:
            True if successful, False otherwise.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.schema_url, timeout=30.0)

                if response.status_code == 200:
                    # Try to parse as YAML (supports both YAML and JSON)
                    self.schema = yaml.safe_load(response.text)
                    self.paths = self.schema.get("paths", {})
                    self.components = self.schema.get("components", {})
                    return True
                else:
                    print(f"Failed to fetch schema: {response.status_code}")
                    return False

        except Exception as e:
            print(f"Error fetching schema: {str(e)}")
            return False

    def get_operations(self) -> List[Dict[str, Any]]:
        """
        Extract all operations from the schema.

        Returns:
            List of operation dictionaries with metadata.
        """
        operations = []

        for path, path_item in self.paths.items():
            for method in ["get", "post", "put", "patch", "delete"]:
                if method in path_item:
                    operation = path_item[method]
                    operation_id = operation.get("operationId")

                    if operation_id:
                        operations.append(
                            {
                                "operation_id": operation_id,
                                "path": path,
                                "method": method.upper(),
                                "summary": operation.get("summary", ""),
                                "description": operation.get("description", ""),
                                "parameters": self._extract_parameters(operation, path_item),
                                "request_body": self._extract_request_body(operation),
                                "responses": operation.get("responses", {}),
                                "tags": operation.get("tags", []),
                            }
                        )

        return operations

    def _extract_parameters(
        self, operation: Dict[str, Any], path_item: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract parameters from operation and path item.

        Returns:
            Dictionary with 'path', 'query', and 'header' parameter lists.
        """
        params = {"path": [], "query": [], "header": []}

        # Get parameters from operation and path level
        all_params = operation.get("parameters", []) + path_item.get("parameters", [])

        for param in all_params:
            # Resolve $ref if present
            if "$ref" in param:
                param = self._resolve_ref(param["$ref"])

            param_in = param.get("in", "query")
            if param_in in params:
                params[param_in].append(
                    {
                        "name": param.get("name"),
                        "required": param.get("required", False),
                        "schema": param.get("schema", {}),
                        "description": param.get("description", ""),
                        "type": self._get_param_type(param.get("schema", {})),
                    }
                )

        return params

    def _extract_request_body(self, operation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract request body schema from operation.

        Returns:
            Request body metadata or None.
        """
        request_body = operation.get("requestBody")
        if not request_body:
            return None

        # Resolve $ref if present
        if "$ref" in request_body:
            request_body = self._resolve_ref(request_body["$ref"])

        content = request_body.get("content", {})

        # Look for JSON content
        json_content = content.get("application/json") or content.get(
            "application/json; charset=utf-8"
        )

        if json_content:
            schema = json_content.get("schema", {})

            # Resolve $ref in schema if present
            if "$ref" in schema:
                schema = self._resolve_ref(schema["$ref"])

            return {
                "required": request_body.get("required", False),
                "schema": schema,
                "properties": self._extract_properties(schema),
            }

        return None

    def _extract_properties(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Extract properties from a schema object."""
        properties = {}

        schema_properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        for prop_name, prop_schema in schema_properties.items():
            # Resolve $ref if present
            if "$ref" in prop_schema:
                prop_schema = self._resolve_ref(prop_schema["$ref"])

            properties[prop_name] = {
                "type": self._get_param_type(prop_schema),
                "required": prop_name in required_fields,
                "description": prop_schema.get("description", ""),
                "schema": prop_schema,
            }

        return properties

    def _get_param_type(self, schema: Dict[str, Any]) -> str:
        """
        Map OpenAPI type to Python type string.

        Args:
            schema: OpenAPI schema object

        Returns:
            Python type string
        """
        if not schema:
            return "string"

        openapi_type = schema.get("type", "string")

        type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict",
        }

        return type_map.get(openapi_type, "str")

    def _resolve_ref(self, ref: str) -> Dict[str, Any]:
        """
        Resolve a $ref to its actual schema.

        Args:
            ref: Reference string (e.g., "#/components/schemas/Model")

        Returns:
            Resolved schema dictionary
        """
        if not ref.startswith("#/"):
            return {}

        # Split ref path and navigate through schema
        parts = ref[2:].split("/")
        current = self.schema

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return {}

        return current if isinstance(current, dict) else {}

    def get_operation_by_id(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific operation by its operation ID.

        Args:
            operation_id: The operation ID to search for

        Returns:
            Operation dictionary or None if not found
        """
        operations = self.get_operations()
        for op in operations:
            if op["operation_id"] == operation_id:
                return op
        return None
