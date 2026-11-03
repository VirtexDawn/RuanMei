from typing import Any, Dict, Optional
import httpx


class HTTPRequest:
    def __init__(
        self,
        base_url: str = "",
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 10.0,
    ):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout

    # --- Synchronous Methods ---

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        with httpx.Client(
            headers=self.headers, timeout=self.timeout
        ) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        with httpx.Client(
            headers=self.headers, timeout=self.timeout
        ) as client:
            response = client.post(url, data=data, json=json)
            response.raise_for_status()
            return response.json()

    # --- Asynchronous Methods ---

    async def async_get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(
            headers=self.headers, timeout=self.timeout
        ) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def async_post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(
            headers=self.headers, timeout=self.timeout
        ) as client:
            response = await client.post(url, data=data, json=json)
            response.raise_for_status()
            return response.json()