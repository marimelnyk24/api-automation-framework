from pytest import assume

from data.test_data import CREATE_POST_PAYLOAD
from endpoints.posts import PostsAPI
from utils.assertions import Assert
from utils.schemas import PostSchema


def test_create_post(posts_api: PostsAPI):
    payload = CREATE_POST_PAYLOAD

    response = posts_api.create_post(payload)
    response_json = response.json()

    Assert.status_code(response, 201)
    PostSchema.validate(response_json)

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