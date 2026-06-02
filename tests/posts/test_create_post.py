from dataclasses import asdict

from data.factories.post_factory import PostFactory
from data.models.post import Post
from endpoints.posts import PostsAPI
from utils.soft_assert import SoftAssert
from utils.schemas import PostSchema


def test_create_post(posts_api: PostsAPI):
    soft = SoftAssert()
    post = PostFactory.create()

    response = posts_api.create_post(asdict(post))

    response.assert_status(201) \
            .as_object() \
            .validate(PostSchema)

    res_post = response.to_model(Post)

    soft \
        .equals(res_post.title, post.title, "title") \
        .equals(res_post.body, post.body, "body") \
        .equals(res_post.userId, post.userId, "userId") \
        .assert_all()


def test_create_post_title_only(posts_api: PostsAPI):
    """Sending only a title should still return 201 (fake API behavior)."""
    soft = SoftAssert()
    post = PostFactory.create(title="Test Title")

    response = posts_api.create_post(asdict(post))

    response.assert_status(201).as_object().validate(PostSchema)

    res_post = response.to_model(Post)
 
    soft \
        .equals(res_post.title, post.title, "title") \
        .assert_all()


def test_create_post_with_extra_fields(posts_api: PostsAPI):
    """Extra unknown fields should be echoed back or silently ignored — not cause an error."""
    post = PostFactory.create()
    payload = {**asdict(post), "extra_field": "unexpected"}
 
    response = posts_api.create_post(payload)
 
    response.assert_status(201).as_object().validate(PostSchema)


def test_create_post_empty_body(posts_api: PostsAPI):
    """Empty JSON object — fake API fakes success; document actual behavior."""
    response = posts_api.create_post({})
 
    # JSONPlaceholder fakes all mutations, so 201 is the realistic expectation.
    # Change to 400 if your real API validates required fields.
    response.assert_status(201).as_object()
