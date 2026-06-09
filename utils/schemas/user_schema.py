from utils.schemas.base_schema import BaseSchema
from utils.schemas.address_schema import AddressSchema
from utils.schemas.company_schema import CompanySchema


class UserSchema(BaseSchema):

    REQUIRED_FIELDS = {
        "id": int,
        "name": str,
        "username": str,
        "email": str,
        "address": dict,
        "phone": str,
        "website": str,
        "company": dict,
    }

    @classmethod
    def validate(cls, data):
        super().validate(data)
        AddressSchema.validate(data["address"])
        CompanySchema.validate(data["company"])