from utils.schemas.base_schema import BaseSchema


class GeoSchema(BaseSchema):

    REQUIRED_FIELDS = {
        "lat": str,
        "lng": str,
    }