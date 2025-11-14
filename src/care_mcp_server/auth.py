"""
Authentication handler for Care API
"""

import httpx
from typing import Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AuthHandler:
    """Handle authentication with Care API"""

    def __init__(self, base_url: str, username: Optional[str] = None, password: Optional[str] = None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None

    async def authenticate(self) -> bool:
        """Authenticate and obtain access token"""
        if not self.username or not self.password:
            logger.warning("No credentials provided for authentication")
            return False

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/auth/login",
                    json={
                        "username": self.username,
                        "password": self.password
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data.get("access") or data.get("access_token")
                    self.refresh_token = data.get("refresh") or data.get("refresh_token")

                    # Set expiry (default 1 hour if not provided)
                    expires_in = data.get("expires_in", 3600)
                    self.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

                    logger.info("✅ Authentication successful")
                    return True
                else:
                    logger.error(f"❌ Authentication failed: HTTP {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    return False

        except Exception as exc:  # noqa: BLE001
            logger.error("❌ Authentication error", exc_info=exc)
            return False

    def is_token_valid(self) -> bool:
        """Check if current token is still valid"""
        if not self.access_token:
            return False

        if not self.token_expiry:
            return True  # No expiry set, assume valid

        # Check if token expires in next 5 minutes
        return datetime.utcnow() < (self.token_expiry - timedelta(minutes=5))

    async def refresh_access_token(self) -> bool:
        """Refresh the access token using refresh token"""
        if not self.refresh_token:
            logger.warning("No refresh token available")
            return await self.authenticate()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/auth/token/refresh",
                    json={"refresh": self.refresh_token},
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data.get("access")

                    expires_in = data.get("expires_in", 3600)
                    self.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

                    logger.info("✅ Token refreshed successfully")
                    return True
                else:
                    logger.error(f"❌ Token refresh failed: HTTP {response.status_code}")
                    # Fall back to re-authentication
                    return await self.authenticate()

        except Exception as exc:  # noqa: BLE001
            logger.error("❌ Token refresh error", exc_info=exc)
            return await self.authenticate()

    async def get_valid_token(self) -> Optional[str]:
        """Get a valid access token, refreshing if necessary"""
        if self.access_token and self.is_token_valid():
            return self.access_token

        if await self.refresh_access_token():
            return self.access_token

        return None

    def get_headers(self) -> dict:
        """Get HTTP headers with authentication"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "care-mcp-server/0.1.0"
        }

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return headers
