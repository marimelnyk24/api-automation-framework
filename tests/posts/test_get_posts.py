from pytest import assume

from utils.assertions import Assert
from utils.schemas import PostSchema


def test_get_posts(posts_api):
    response = posts_api.get_posts()

    response.assert_status_code(200) \
            .expect_list() \
            .not_empty() \
            .each_schema(PostSchema, limit=5)

def test_get_single_post(posts_api):
    response = posts_api.get_post(1)

    response.assert_status_code(200) \
            .expect_object() \
            .schema(PostSchema)

    data = response.json

    with assume:
        Assert.equals(
            data["id"],
            1,
            "id"
        )