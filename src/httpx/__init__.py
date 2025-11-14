"""Minimal httpx-compatible asynchronous client for offline environments.

This simplified implementation provides the subset of the httpx API required by the project.
It supports basic JSON requests and responses using Python's standard library.
"""

from __future__ import annotations

import asyncio
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


class HTTPStatusError(Exception):
    """Exception raised when a request returns an unsuccessful status code."""

    def __init__(self, message: str, response: "Response") -> None:
        super().__init__(message)
        self.response = response


@dataclass
class Response:
    """Simple HTTP response wrapper."""

    status_code: int
    _content: bytes
    headers: Dict[str, str]

    def json(self) -> Any:
        """Decode the response body as JSON."""

        if not self._content:
            return None
        return json.loads(self.text)

    @property
    def text(self) -> str:
        """Return the response body as a string."""

        return self._content.decode("utf-8", errors="replace")

    def raise_for_status(self) -> None:
        """Raise HTTPStatusError if the response indicates an error."""

        if self.status_code >= 400:
            raise HTTPStatusError(f"HTTP {self.status_code}", self)


class AsyncClient:
    """Very small asynchronous HTTP client compatible with httpx.AsyncClient."""

    def __init__(self, base_url: str = "", headers: Optional[Dict[str, str]] = None, timeout: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout

    async def __aenter__(self) -> "AsyncClient":  # noqa: D401
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001, ANN201
        return None

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Response:
        return await self._request("GET", url, params=params, **kwargs)

    async def post(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Response:
        return await self._request("POST", url, json=json, params=params, **kwargs)

    async def put(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Response:
        return await self._request("PUT", url, json=json, params=params, **kwargs)

    async def patch(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Response:
        return await self._request("PATCH", url, json=json, params=params, **kwargs)

    async def delete(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Response:
        return await self._request("DELETE", url, params=params, **kwargs)

    async def _request(
        self,
        method: str,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        **_: Any,
    ) -> Response:
        full_url = self._build_url(url, params)
        data: Optional[bytes] = None
        final_headers = {"Accept": "application/json", **self.headers}
        if headers:
            final_headers.update(headers)

        if json is not None:
            data = json.dumps(json).encode("utf-8")
            final_headers.setdefault("Content-Type", "application/json")

        request = urllib.request.Request(full_url, data=data, headers=final_headers, method=method)
        return await asyncio.to_thread(self._perform_request, request, timeout or self.timeout)

    def _build_url(self, url: str, params: Optional[Dict[str, Any]]) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            base = url
        else:
            if url.startswith("/"):
                base = f"{self.base_url}{url}"
            else:
                base = f"{self.base_url}/{url}" if self.base_url else url

        if params:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            separator = "&" if urllib.parse.urlparse(base).query else "?"
            base = f"{base}{separator}{query}"
        return base

    def _perform_request(self, request: urllib.request.Request, timeout: float) -> Response:
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                content = response.read()
                headers = {k: v for k, v in response.getheaders()}
                return Response(status_code=response.status, _content=content, headers=headers)
        except urllib.error.HTTPError as exc:
            content = exc.read()
            headers = {k: v for k, v in exc.headers.items()} if exc.headers else {}
            response = Response(status_code=exc.code, _content=content, headers=headers)
            raise HTTPStatusError(f"HTTP {exc.code}", response) from None
        except urllib.error.URLError as exc:  # noqa: F841
            raise RuntimeError(str(exc))


__all__ = ["AsyncClient", "HTTPStatusError", "Response"]
