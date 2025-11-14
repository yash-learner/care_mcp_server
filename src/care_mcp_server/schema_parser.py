"""
OpenAPI schema parser for Care API
"""

import httpx
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class SchemaParser:
    """Parse OpenAPI/Swagger schema"""

    def __init__(self, schema_url: str):
        self.schema_url = schema_url
        self.schema: Optional[Dict[str, Any]] = None

    async def load_schema(self) -> bool:
        """Load OpenAPI schema from URL"""
        try:
            async with httpx.AsyncClient() as client:
                logger.info("📥 Fetching schema from %s", self.schema_url)

                response = await client.get(
                    self.schema_url,
                    headers={"Accept": "application/json"},
                    timeout=30.0,
                )

                response.raise_for_status()
                self.schema = response.json()

                info = self.schema.get("info", {})
                logger.info("✅ Loaded schema: %s", info.get("title", "API"))
                logger.info("   Version: %s", info.get("version", "unknown"))
                logger.info("   Endpoints: %s", len(self.schema.get("paths", {})))

                return True

        except Exception as exc:  # noqa: BLE001
            logger.error("❌ Failed to load schema", exc_info=exc)
            return False

    def get_paths(self) -> Dict[str, Any]:
        """Get all API paths"""
        if not self.schema:
            return {}
        return self.schema.get("paths", {})

    def get_operation(self, path: str, method: str) -> Optional[Dict[str, Any]]:
        """Get specific operation details"""
        paths = self.get_paths()
        path_item = paths.get(path, {})
        return path_item.get(method.lower())

    @staticmethod
    def map_openapi_type(openapi_type: str, fmt: Optional[str] = None) -> type:  # noqa: ARG004
        """Map OpenAPI types to Python types"""
        type_map: Dict[str, type] = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        return type_map.get(openapi_type, str)

    def extract_parameters(self, operation: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract parameters from operation"""
        params: Dict[str, Dict[str, Any]] = {}

        # Path/query parameters
        for param in operation.get("parameters", []):
            param_name = param.get("name")
            param_in = param.get("in")
            required = param.get("required", False)
            description = param.get("description", "")

            schema = param.get("schema", {})
            param_type = schema.get("type", "string")

            params[param_name] = {
                "type": self.map_openapi_type(param_type),
                "required": required,
                "description": description,
                "location": param_in,
            }

        # Request body
        request_body = operation.get("requestBody", {})
        if request_body:
            content = request_body.get("content", {})
            json_schema = content.get("application/json", {}).get("schema", {})

            if json_schema.get("type") == "object":
                properties = json_schema.get("properties", {})
                required_fields = json_schema.get("required", [])

                for prop_name, prop_def in properties.items():
                    params[prop_name] = {
                        "type": self.map_openapi_type(prop_def.get("type", "string")),
                        "required": prop_name in required_fields,
                        "description": prop_def.get("description", ""),
                        "location": "body",
                    }

        return params
