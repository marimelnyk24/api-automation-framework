from typing import Any
from urllib.parse import urljoin

import requests
from requests import Response, Session
from loguru import logger


class APIClient:

    def __init__(
        self,
        base_url: str,
        timeout: int = 10
    ):
        self.base_url = base_url
        self.timeout = timeout

        self.session = Session()

        # default headers
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> Response:

        url = urljoin(self.base_url, endpoint)

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

        except requests.RequestException as error:
            logger.exception(
                f"Request failed: {method.upper()} {url}"
            )
            raise

        logger.info(
            f"Response status: {response.status_code}"
        )

        if response.status_code >= 400:
            logger.error(
                f"Error response body: {response.text}"
            )

        return response

    def get(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> Response:

        return self._request(
            "GET",
            endpoint,
            **kwargs
        )

    def post(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> Response:

        return self._request(
            "POST",
            endpoint,
            **kwargs
        )

    def put(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> Response:

        return self._request(
            "PUT",
            endpoint,
            **kwargs
        )

    def delete(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> Response:

        return self._request(
            "DELETE",
            endpoint,
            **kwargs
        )