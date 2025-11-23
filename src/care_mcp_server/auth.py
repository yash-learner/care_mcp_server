"""Authentication handler for Care API."""

import time
from typing import Optional, Dict
import httpx
from .config import Config


class AuthHandler:
    """Handles authentication and token management for Care API."""

    def __init__(self, config: Config):
        """Initialize auth handler with configuration."""
        self.config = config
        self.access_token: Optional[str] = config.care_access_token
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[float] = None
        self.default_token_lifetime = 3600  # 1 hour in seconds

    async def authenticate(self) -> bool:
        """
        Authenticate with Care API.

        Returns:
            True if authentication successful, False otherwise.
        """
        # If we already have a token, check if it's still valid
        if self.access_token:
            if not self._is_token_expired():
                return True

        # If we have username/password, login
        if self.config.care_username and self.config.care_password:
            return await self._login()

        # If we only have a token that's expired, we can't refresh without credentials
        if self.access_token and self._is_token_expired():
            print("Warning: Access token expired and no credentials available for refresh")
            return False

        return False

    async def _login(self) -> bool:
        """
        Login to Care API with username and password.

        Returns:
            True if login successful, False otherwise.
        """
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                print(f"   Attempting login to: {self.config.login_url}")
                print(f"   Username: {self.config.care_username}")

                response = await client.post(
                    self.config.login_url,
                    json={
                        "username": self.config.care_username,
                        "password": self.config.care_password,
                    },
                    timeout=30.0,
                )

                print(f"   Response status: {response.status_code}")
                print(f"   Response URL: {response.url}")
                if response.headers.get('location'):
                    print(f"   Redirect location: {response.headers.get('location')}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        self.access_token = data.get("access")
                        self.refresh_token = data.get("refresh")

                        if not self.access_token:
                            print(f"   Warning: No access token in response: {data}")
                            return False

                        # Set token expiry (default 1 hour from now)
                        self.token_expiry = time.time() + self.default_token_lifetime

                        return True
                    except Exception as json_error:
                        print(f"   Error parsing JSON response: {json_error}")
                        print(f"   Raw response: {response.text}")
                        return False
                else:
                    print(f"Login failed: {response.status_code} - {response.text}")
                    return False

        except Exception as e:
            print(f"Login error: {str(e)}")
            return False

    def _is_token_expired(self) -> bool:
        """Check if the current token is expired."""
        if not self.token_expiry:
            # If we don't know the expiry, assume it might be expired
            return False
        return time.time() >= self.token_expiry

    async def refresh_access_token(self) -> bool:
        """
        Refresh the access token using refresh token.

        Returns:
            True if refresh successful, False otherwise.
        """
        if not self.refresh_token:
            # No refresh token, try to re-login
            return await self._login()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.config.care_base_url.rstrip('/')}/api/v1/auth/token/refresh",
                    json={"refresh": self.refresh_token},
                    timeout=30.0,
                )

                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data.get("access")
                    self.token_expiry = time.time() + self.default_token_lifetime
                    return True
                else:
                    # Refresh failed, try to re-login
                    return await self._login()

        except Exception as e:
            print(f"Token refresh error: {str(e)}")
            # Try to re-login as fallback
            return await self._login()

    async def get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with authentication token.

        Automatically refreshes token if expired.

        Returns:
            Dictionary with Authorization header.
        """
        # Check if token is expired and refresh if needed
        if self._is_token_expired():
            await self.refresh_access_token()

        if not self.access_token:
            await self.authenticate()

        return {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
