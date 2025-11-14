import asyncio

from care_mcp_server.auth import AuthHandler


def test_get_valid_token_without_credentials():
    handler = AuthHandler(base_url="https://example.com")
    token = asyncio.run(handler.get_valid_token())
    assert token is None


def test_get_headers_includes_authorization():
    handler = AuthHandler(base_url="https://example.com")
    handler.access_token = "token"
    headers = handler.get_headers()
    assert headers["Authorization"] == "Bearer token"
