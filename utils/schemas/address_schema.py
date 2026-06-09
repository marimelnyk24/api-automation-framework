from utils.schemas.base_schema import BaseSchema
from utils.schemas.geo_schema import GeoSchema


class AddressSchema(BaseSchema):

    REQUIRED_FIELDS = {
        "street": str,
        "suite": str,
        "city": str,
        "zipcode": str,
        "geo": dict,
    }

    @classmethod
    def validate(cls, data):
        super().validate(data)
        GeoSchema.validate(data["geo"])