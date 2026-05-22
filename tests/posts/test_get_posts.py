from pytest import assume

from utils.assertions import Assert
from utils.schemas import PostSchema


def test_get_posts(posts_api):
    response = posts_api.get_posts()
    response_json = response.json()

    Assert.status_code(response, 200)

    assert isinstance(response_json, list)
    assert response_json, "Response should not be empty"

    for post in response_json[:3]:
        PostSchema.validate(post)

def test_get_single_post(posts_api):
    response = posts_api.get_post(1)
    response_json = response.json()

    Assert.status_code(response, 200)
    PostSchema.validate(response_json)

    with assume:
        Assert.equals(
            response_json["id"],
            1,
            "id"
        )