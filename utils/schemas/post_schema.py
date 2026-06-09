from utils.schemas.base_schema import BaseSchema


class PostSchema(BaseSchema):

    REQUIRED_FIELDS = {
        "id": int,
        "title": str,
        "body": str,
        "userId": int
    }