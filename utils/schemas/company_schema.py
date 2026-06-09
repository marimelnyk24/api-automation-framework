from utils.schemas.base_schema import BaseSchema

class CompanySchema(BaseSchema):

    REQUIRED_FIELDS = {
        "name": str,
        "catchPhrase": str,
        "bs": str,
    }