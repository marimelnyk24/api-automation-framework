from typing import Any
from urllib.parse import urlparse

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from loguru import logger
from urllib3.util.retry import Retry

from utils.api_response import APIResponse


class APIClient:

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.3
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = Session()

        # default headers
        self.session.headers.update({
            "Content-Type": "application/json"
        })

        retry_strategy = Retry(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST", "PUT", "DELETE"}),
            raise_on_status=False
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _build_url(self, endpoint: str) -> str:
        parsed_endpoint = urlparse(endpoint)

        if parsed_endpoint.scheme or parsed_endpoint.netloc:
            raise ValueError(
                f"Endpoint must be a relative path, got: {endpoint}"
            )

        normalized_endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{normalized_endpoint}"

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> APIResponse:

        url = self._build_url(endpoint)

        kwargs.setdefault(
            "timeout",
            self.timeout
        )

        payload = kwargs.get("json")
        params = kwargs.get("params")

        logger.info(
            f"{method.upper()} request to {url}"
        )

        if params:
            logger.info(f"Query params: {params}")

        if payload:
            logger.info(f"Payload: {payload}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                **kwargs
            )

        except requests.RequestException:
            logger.exception(
                f"Request failed: {method.upper()} {url}"
            )
            raise

        logger.info(
            f"Response status: {response.status_code} | "
            f"elapsed={response.elapsed.total_seconds():.3f}s"
        )

        if response.status_code >= 400:
            logger.error(
                f"Error response body: {response.text}"
            )

        return APIResponse(response)

    def get(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> APIResponse:

        return self._request(
            "GET",
            endpoint,
            **kwargs
        )

    def post(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> APIResponse:

        return self._request(
            "POST",
            endpoint,
            **kwargs
        )

    def put(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> APIResponse:

        return self._request(
            "PUT",
            endpoint,
            **kwargs
        )

    def delete(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> APIResponse:

        return self._request(
            "DELETE",
            endpoint,
            **kwargs
        )
