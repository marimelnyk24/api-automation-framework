from loguru import logger

from clients.api_client import APIClient


class PostsAPI:

    POSTS = "/posts"

    def __init__(self, client: APIClient):
        self.client = client

    def get_posts(self):
        logger.info("Fetching all posts")
        return self.client.get(self.POSTS)

    def get_post(self, post_id: int):
        logger.info(f"Fetching post with ID {post_id}")
        return self.client.get(f"{self.POSTS}/{post_id}")

    def create_post(self, payload: dict):
        logger.info(
            f"Creating post | keys={list(payload.keys())}"
        )

        return self.client.post(
            self.POSTS,
            json=payload
        )