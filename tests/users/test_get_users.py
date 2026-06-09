from utils.schemas.user_schema import UserSchema


def test_get_users(users_api):
    response = users_api.get_users()

    response.assert_status(200) \
            .as_list() \
            .not_empty() \
            .length(10) \
            .validate(UserSchema)
