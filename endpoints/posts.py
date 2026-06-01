from loguru import logger

from clients.api_client import APIClient
from core.response import Response


class PostsAPI:

    POSTS = "/posts"

    def __init__(self, client: APIClient):
        self.client = client

    def get_posts(self) -> Response:
        logger.info("Fetching all posts")
        return self.client.get(self.POSTS)

    def get_post(self, post_id: int | str) -> Response:
        logger.info(f"Fetching post with ID {post_id}")
        return self.client.get(f"{self.POSTS}/{post_id}")

    def create_post(self, payload: dict) -> Response:
        logger.info(
            f"Creating post | keys={list(payload.keys())}"
        )

        return self.client.post(
            self.POSTS,
            json=payload
        )
    
    def filter_posts(self, params: dict = None) -> Response:
        logger.info(
            f"Filtering posts with params: {params}"
        )
        return self.client.get(
            self.POSTS,
            params=params
        )
    
    def get_post_comments(self, post_id: int | str) -> Response:
        logger.info(f"Fetching comments for post ID {post_id}")
        return self.client.get(f"{self.POSTS}/{post_id}/comments")
