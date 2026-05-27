from pytest import assume

from data.test_data import CREATE_POST_PAYLOAD
from endpoints.posts import PostsAPI
from utils.assertions import Assert
from utils.schemas import PostSchema


def test_create_post(posts_api: PostsAPI):
    payload = CREATE_POST_PAYLOAD

    response = posts_api.create_post(payload)

    response.assert_status_code(201)
    response.assert_schema(PostSchema)

    data = response.json

    with assume:
        Assert.equals(
            data["title"],
            payload["title"],
            "title"
        )

    with assume:
        Assert.equals(
            data["body"],
            payload["body"],
            "body"
        )