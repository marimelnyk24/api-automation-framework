def test_delete_post(posts_api):
    response = posts_api.delete_post(1)

    response.assert_status(200).as_object().is_empty()


def test_delete_non_existent_post(posts_api):
    response = posts_api.delete_post(9999)

    # JSONPlaceholder returns 200 even for non-existent resources, but real APIs might return 404.
    response.assert_status(200).as_object().is_empty()