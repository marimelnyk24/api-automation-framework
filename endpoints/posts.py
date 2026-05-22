from clients.api_client import APIClient

class PostsAPI:

    POSTS = "/posts"

    def __init__(self, client: APIClient):
        self.client = client

    def get_posts(self):
        return self.client.get(self.POSTS)
    
    def get_post(self, post_id):
        return self.client.get(f"{self.POSTS}/{post_id}")

    def create_post(self, payload: dict):
        return self.client.post(
            self.POSTS,
            json=payload
        )
    