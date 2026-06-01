import pytest
from pytest import assume

from data.models.comment import Comment
from data.models.post import Post
from data.test_data import INVALID_POST_ID, INVALID_POST_ID_STR, INVALID_USER_ID
from utils.assertions import Assert
from utils.schemas import PostSchema


def test_get_posts(posts_api):
    response = posts_api.get_posts()

    response.assert_status_code(200) \
            .expect_list() \
            .not_empty() \
            .expect_list_length(100) \
            .each_schema(PostSchema, limit=5)

def test_get_single_post(posts_api):
    response = posts_api.get_post(1)

    response.assert_status_code(200) \
            .expect_object() \
            .schema(PostSchema)

    post = response.to_model(Post)

    with assume:
        Assert.equals(
            post.id,
            1,
            "id"
        )


@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_get_post_boundary_ids(posts_api, post_id):
    """First, middle and last posts must all return 200."""
    response = posts_api.get_post(post_id)
 
    response.assert_status_code(200) \
            .expect_object() \
            .schema(PostSchema)
    
    post = response.to_model(Post)
 
    with assume:
        Assert.equals(post.id, post_id, "id")


def test_filter_posts_by_user_id(posts_api):
    """userId=1 must return only posts belonging to that user."""
    response = posts_api.filter_posts(params={"userId": 1})
 
    response.assert_status_code(200) \
            .expect_list() \
            .not_empty()
    
    posts = response.to_models(Post)
 
    for post in posts:
        with assume:
            Assert.equals(post.userId, 1, "userId")


def test_get_post_comments(posts_api):
    """/posts/1/comments must return comments for postId=1."""
    response = posts_api.get_post_comments(1)
 
    response.assert_status_code(200) \
            .expect_list() \
            .not_empty()
    
    comments = response.to_models(Comment)
 
    for comment in comments:
        with assume:
            Assert.equals(comment.postId, 1, "postId")


def test_get_non_existent_post_returns_404(posts_api):
    response = posts_api.get_post(INVALID_POST_ID)
 
    response.assert_status_code(404).expect_object()


@pytest.mark.parametrize("post_id", [0, 101])
def test_get_out_of_range_post_ids(posts_api, post_id):
    response = posts_api.get_post(post_id)
 
    response.assert_status_code(404)


def test_get_post_with_string_id_returns_404(posts_api):
    response = posts_api.get_post(INVALID_POST_ID_STR)
 
    response.assert_status_code(404)
 
 
def test_get_post_with_negative_id_returns_404(posts_api):
    response = posts_api.get_post(-1)
 
    response.assert_status_code(404)


def test_filter_posts_non_existent_user_returns_empty(posts_api):
    response = posts_api.filter_posts(params={"userId": INVALID_USER_ID})
 
    response.assert_status_code(200).expect_list()
 
    assert response.json == [], (
        f"Expected empty list for non-existent userId, got {len(response.json)} items"
    )
 
 
def test_filter_posts_invalid_user_id_type(posts_api):
    """A non-numeric userId should return an empty list or 200 without results."""
    response = posts_api.filter_posts(params={"userId": "abc"})
 
    response.assert_status_code(200).expect_list()
 
    assert response.json == [], (
        "Expected empty list for non-numeric userId"
    )