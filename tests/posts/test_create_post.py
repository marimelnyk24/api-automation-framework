from pytest import assume

from data.test_data import CREATE_POST_PAYLOAD
from endpoints.posts import PostsAPI
from utils.assertions import Assert


def test_create_post(posts_api: PostsAPI):
    payload = CREATE_POST_PAYLOAD

    response = posts_api.create_post(payload)
    response_json = response.json()

    Assert.status_code(response, 201)

    with assume:
        Assert.equals(
            response_json["title"],
            payload["title"],
            "title"
        )

    with assume:
        Assert.equals(
            response_json["body"],
            payload["body"],
            "body"
        )

    with assume:
        Assert.has_key(response_json, "id")