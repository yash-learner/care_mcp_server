"""MCP tool generator for Care API operations."""
from typing import Dict, Any, List, Callable
import httpx
from mcp.server.fastmcp import FastMCP
from .auth import AuthHandler
from .schema_parser import SchemaParser
from .whitelist import WhitelistManager
from .enhancements import EnhancementManager
from .config import Config


class ToolGenerator:
    """Generate MCP tools from OpenAPI operations."""
    
    def __init__(
        self,
        config: Config,
        auth_handler: AuthHandler,
        schema_parser: SchemaParser,
        whitelist_manager: WhitelistManager,
        enhancement_manager: EnhancementManager,
        mcp: FastMCP
    ):
        """Initialize tool generator with dependencies."""
        self.config = config
        self.auth_handler = auth_handler
        self.schema_parser = schema_parser
        self.whitelist_manager = whitelist_manager
        self.enhancement_manager = enhancement_manager
        self.mcp = mcp
        self.generated_count = 0
    
    async def generate_tools(self) -> int:
        """
        Generate and register MCP tools for all whitelisted operations.
        
        Returns:
            Number of tools generated
        """
        operations = self.schema_parser.get_operations()
        
        for operation in operations:
            operation_id = operation["operation_id"]
            
            # Check if operation is whitelisted
            if not self.whitelist_manager.is_allowed(operation_id):
                continue
            
            # Generate and register tool
            await self._generate_tool(operation)
            self.generated_count += 1
        
        return self.generated_count
    
    async def _generate_tool(self, operation: Dict[str, Any]) -> None:
        """
        Generate a single MCP tool from an operation.
        
        Args:
            operation: Operation metadata from schema parser
        """
        operation_id = operation["operation_id"]
        path = operation["path"]
        method = operation["method"]
        parameters = operation["parameters"]
        request_body = operation["request_body"]
        
        # Get enhancement metadata
        enhancement = self.enhancement_manager.get_enhancement(operation_id)
        
        # Determine tool name and description
        if enhancement:
            tool_name = operation_id
            tool_description = f"{enhancement.title}\n\n{enhancement.description}"
        else:
            tool_name = operation_id
            tool_description = operation.get("summary") or operation.get("description") or f"Execute {operation_id}"
        
        # Create the tool function
        tool_func = self._create_tool_function(
            operation_id=operation_id,
            path=path,
            method=method,
            parameters=parameters,
            request_body=request_body
        )
        
        # Register with FastMCP
        self.mcp.tool(name=tool_name, description=tool_description)(tool_func)
    
    def _create_tool_function(
        self,
        operation_id: str,
        path: str,
        method: str,
        parameters: Dict[str, List[Dict[str, Any]]],
        request_body: Any
    ) -> Callable:
        """
        Create an async function for the API operation.
        
        Args:
            operation_id: Operation ID
            path: API path
            method: HTTP method
            parameters: Parameters metadata
            request_body: Request body metadata
            
        Returns:
            Async function for the operation
        """
        async def api_call(**kwargs) -> Dict[str, Any]:
            """Execute API call with provided parameters."""
            try:
                # Separate parameters by location
                path_params = {}
                query_params = {}
                body_data = {}
                
                # Process path parameters
                for param in parameters.get("path", []):
                    param_name = param["name"]
                    if param_name in kwargs:
                        path_params[param_name] = kwargs[param_name]
                
                # Process query parameters
                for param in parameters.get("query", []):
                    param_name = param["name"]
                    if param_name in kwargs:
                        query_params[param_name] = kwargs[param_name]
                
                # Process request body
                if request_body:
                    # Collect all body parameters
                    for key, value in kwargs.items():
                        # If not a path or query param, it's likely a body param
                        if key not in path_params and key not in query_params:
                            body_data[key] = value
                
                # Build URL with path parameters
                url = self._build_url(path, path_params)
                
                # Get authentication headers
                headers = await self.auth_handler.get_headers()
                
                # Make HTTP request
                async with httpx.AsyncClient() as client:
                    if method == "GET":
                        response = await client.get(
                            url, 
                            headers=headers, 
                            params=query_params,
                            timeout=30.0
                        )
                    elif method == "POST":
                        response = await client.post(
                            url,
                            headers=headers,
                            params=query_params,
                            json=body_data if body_data else None,
                            timeout=30.0
                        )
                    elif method == "PUT":
                        response = await client.put(
                            url,
                            headers=headers,
                            params=query_params,
                            json=body_data if body_data else None,
                            timeout=30.0
                        )
                    elif method == "PATCH":
                        response = await client.patch(
                            url,
                            headers=headers,
                            params=query_params,
                            json=body_data if body_data else None,
                            timeout=30.0
                        )
                    elif method == "DELETE":
                        response = await client.delete(
                            url,
                            headers=headers,
                            params=query_params,
                            timeout=30.0
                        )
                    else:
                        return {
                            "success": False,
                            "error": f"Unsupported HTTP method: {method}"
                        }
                
                # Return structured response
                if response.status_code >= 200 and response.status_code < 300:
                    try:
                        data = response.json()
                    except:
                        data = response.text
                    
                    return {
                        "success": True,
                        "status": response.status_code,
                        "data": data
                    }
                else:
                    return {
                        "success": False,
                        "status": response.status_code,
                        "error": response.text
                    }
                    
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Set function metadata
        api_call.__name__ = operation_id
        
        return api_call
    
    def _build_url(self, path: str, path_params: Dict[str, Any]) -> str:
        """
        Build full URL with path parameters.
        
        Args:
            path: API path template (e.g., "/api/v1/facility/{id}/")
            path_params: Path parameter values
            
        Returns:
            Full URL with parameters substituted
        """
        # Replace path parameters
        url_path = path
        for key, value in path_params.items():
            url_path = url_path.replace(f"{{{key}}}", str(value))
        
        # Combine with base URL
        base_url = self.config.care_base_url.rstrip("/")
        return f"{base_url}{url_path}"
