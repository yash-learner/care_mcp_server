"""
MCP tool generator from OpenAPI operations
"""

from typing import Any, Callable, Dict, Optional

import httpx
from mcp.server.fastmcp import FastMCP

from .auth import AuthHandler
from .enhancements import EnhancementManager
from .schema_parser import SchemaParser
from .whitelist import WhitelistManager
import logging

logger = logging.getLogger(__name__)


class ToolGenerator:
    """Generate MCP tools from OpenAPI schema"""

    def __init__(
        self,
        schema_parser: SchemaParser,
        auth_handler: AuthHandler,
        base_url: str,
        whitelist: WhitelistManager,
        enhancements: EnhancementManager,
        mcp_server_name: str = "Care API",
    ):
        self.schema_parser = schema_parser
        self.auth_handler = auth_handler
        self.base_url = base_url
        self.whitelist = whitelist
        self.enhancements = enhancements
        self.mcp = FastMCP(mcp_server_name)
        self.http_client: Optional[httpx.AsyncClient] = None

    def _create_tool_function(
        self,
        path: str,
        method: str,
        operation: Dict[str, Any],
        params: Dict[str, Dict[str, Any]],
    ) -> Callable[..., Any]:
        """Create dynamic function for API call"""

        async def api_call(**kwargs: Any) -> Dict[str, Any]:
            """Dynamic API call"""

            # Initialize HTTP client if needed
            if not self.http_client:
                self.http_client = httpx.AsyncClient(
                    base_url=self.base_url,
                    headers=self.auth_handler.get_headers(),
                    timeout=60.0,
                )

            try:
                # Separate parameters
                path_params: Dict[str, Any] = {}
                query_params: Dict[str, Any] = {}
                body_data: Dict[str, Any] = {}

                for key, value in kwargs.items():
                    if key not in params:
                        continue

                    location = params[key].get("location", "body")

                    if location == "path":
                        path_params[key] = value
                    elif location == "query":
                        query_params[key] = value
                    else:
                        body_data[key] = value

                # Build URL
                url = path
                for key, value in path_params.items():
                    url = url.replace(f"{{{key}}}", str(value))

                # Make request
                if method == "get":
                    response = await self.http_client.get(url, params=query_params)
                elif method == "post":
                    response = await self.http_client.post(url, json=body_data, params=query_params)
                elif method == "put":
                    response = await self.http_client.put(url, json=body_data, params=query_params)
                elif method == "patch":
                    response = await self.http_client.patch(url, json=body_data, params=query_params)
                elif method == "delete":
                    response = await self.http_client.delete(url, params=query_params)
                else:
                    return {"success": False, "error": f"Unsupported method: {method}"}

                response.raise_for_status()

                return {
                    "success": True,
                    "status": response.status_code,
                    "data": response.json(),
                }

            except httpx.HTTPStatusError as exc:
                return {
                    "success": False,
                    "status": exc.response.status_code,
                    "error": f"HTTP {exc.response.status_code}",
                    "detail": exc.response.text[:500],
                }

            except Exception as exc:  # noqa: BLE001
                return {
                    "success": False,
                    "error": "Request failed",
                    "detail": str(exc),
                }

        # Set function metadata
        operation_id = operation.get("operationId", f"{method}_{path}")
        enhancement = self.enhancements.get_enhancement(operation_id)

        if enhancement:
            title = enhancement.title
            description = enhancement.description
        else:
            title = operation.get("summary", operation_id)
            description = operation.get("description", "")

        api_call.__name__ = operation_id
        api_call.__doc__ = f"""{title}

{description}

API: {method.upper()} {path}
"""

        return api_call

    def generate_tools(self) -> int:
        """Generate all whitelisted MCP tools"""
        tool_count = 0
        paths = self.schema_parser.get_paths()

        for path, path_item in paths.items():
            for method in ["get", "post", "put", "patch", "delete"]:
                operation = path_item.get(method)

                if not operation:
                    continue

                operation_id = operation.get("operationId")

                # Check whitelist
                if not self.whitelist.is_allowed(operation_id):
                    continue

                # Extract parameters
                params = self.schema_parser.extract_parameters(operation)

                # Create and register tool
                tool_func = self._create_tool_function(path, method, operation, params)
                self.mcp.tool()(tool_func)

                tool_count += 1
                logger.info("  ✅ %s", operation_id)

        return tool_count

    def get_mcp_server(self) -> FastMCP:
        """Get the FastMCP server instance"""
        return self.mcp
