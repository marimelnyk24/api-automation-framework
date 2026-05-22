from pytest import assume

from utils.assertions import Assert


def test_get_posts(posts_api):
    response = posts_api.get_posts()

    Assert.status_code(response, 200)


def test_get_single_post(posts_api):
    response = posts_api.get_post(1)

    Assert.status_code(response, 200)

    with assume:
        Assert.equals(
            response.json()["id"],
            1,
            "id"
        )