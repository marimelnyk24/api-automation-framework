from pytest import assume

from dataclasses import asdict

from data.factories.post_factory import PostFactory
from data.models.post import Post
from endpoints.posts import PostsAPI
from utils.assertions import Assert
from utils.schemas import PostSchema


def test_create_post(posts_api: PostsAPI):
    post = PostFactory.create()

    response = posts_api.create_post(asdict(post))

    response.assert_status_code(201) \
            .expect_object() \
            .schema(PostSchema)

    res_post = Post(**response.json)

    with assume:
        Assert.equals(
            res_post.title,
            post.title,
            "title"
        )

    with assume:
        Assert.equals(
            res_post.body,
            post.body,
            "body"
        )
    
    with assume:
        Assert.equals(
            res_post.userId,
            post.userId,
            "userId"
        )


def test_create_post_title_only(posts_api: PostsAPI):
    """Sending only a title should still return 201 (fake API behavior)."""
    post = PostFactory.create(title="Test Title")

    response = posts_api.create_post(asdict(post))

    response.assert_status_code(201).expect_object()

    res_post = Post(**response.json)
 
    with assume:
        Assert.equals(res_post.title, post.title, "title")


def test_create_post_with_extra_fields(posts_api: PostsAPI):
    """Extra unknown fields should be echoed back or silently ignored — not cause an error."""
    post = PostFactory.create()
    payload = {**asdict(post), "extra_field": "unexpected"}
 
    response = posts_api.create_post(payload)
 
    response.assert_status_code(201).expect_object()


def test_create_post_empty_body(posts_api: PostsAPI):
    """Empty JSON object — fake API fakes success; document actual behavior."""
    response = posts_api.create_post({})
 
    # JSONPlaceholder fakes all mutations, so 201 is the realistic expectation.
    # Change to 400 if your real API validates required fields.
    response.assert_status_code(201).expect_object()
