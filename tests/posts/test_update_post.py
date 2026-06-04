from data.models.post import Post
from utils.schemas import PostSchema
from utils.soft_assert import SoftAssert


def test_put_full_update(posts_api):
    soft = SoftAssert()
    payload = {
        "id": 1,
        "title": "updated",
        "body": "updated body",
        "userId": 1
    }

    response = posts_api.update_post(1, payload)

    response.assert_status(200) \
            .as_object() \
            .validate(PostSchema)

    updated = response.to_model(Post)

    soft \
        .equals(updated.title, payload["title"], "title") \
        .equals(updated.body, payload["body"], "body") \
        .assert_all()


def test_put_non_existent_post(posts_api):
    payload = {
        "id": 9999,
        "title": "x",
        "body": "y",
        "userId": 1
    }

    response = posts_api.update_post(9999, payload)

    response.assert_status(500)


def test_patch_title_only(posts_api):
    soft = SoftAssert()
    response = posts_api.patch_post(1, {"title": "patched"})

    response.assert_status(200).as_object()

    updated = response.to_model(Post)
    
    soft.equals(updated.title, "patched", "title") \
        .assert_all()
    

def test_patch_unknown_field(posts_api):
    payload = {"foo": "bar"}

    response = posts_api.patch_post(1, payload)
    response.assert_status(200).as_object()

    updated = response.to_model(Post)

    # known field still valid
    assert updated.id == 1

    # unknown field is echoed back
    assert response.json["foo"] == "bar"