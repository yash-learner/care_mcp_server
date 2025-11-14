"""Minimal FastMCP stub used for testing.

This stub mimics the interface required by the project without providing full MCP functionality.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict


class FastMCP:
    """Very small stub of the FastMCP server used for local tests."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._tools: Dict[str, Callable[..., Awaitable[Any]]] = {}

    def tool(self) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
        """Decorator that registers a callable as an MCP tool."""

        def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
            self._tools[func.__name__] = func
            return func

        return decorator

    def run(self, transport: str = "stdio") -> None:  # noqa: ARG002
        """Run the stub server.

        The real implementation would start an MCP event loop. For tests we simply verify
        that the method can be called without raising errors.
        """

        # No-op for the stub implementation.
        return None

    @property
    def tools(self) -> Dict[str, Callable[..., Awaitable[Any]]]:
        """Expose registered tools for assertions in tests."""

        return self._tools
