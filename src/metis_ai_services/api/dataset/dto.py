"""Parsers and serializers for /datasets API endpoints."""
import re

from flask_restx import Model
from flask_restx.reqparse import RequestParser
from flask_restx.fields import String, Boolean, Integer, List, Nested
from flask_restx.inputs import positive


def validate_name(name):
    """Validation method for a string containing only letters, numbers, '-' and '_'."""
    if not re.compile(r"^[\w-]+$").match(name):
        raise ValueError(
            f"'{name}' contains one or more invalid characters. Widget name must "
            "contain only letters, numbers, hyphen and underscore characters."
        )
    return name


# bundle_errors=True: all error messages reported for all arguments in our request parser.
create_dataset_reqparser = RequestParser(bundle_errors=True)
# Add Argument Ref.
create_dataset_reqparser.add_argument(name="ds_name", type=str, location="form", required=True, nullable=False)
create_dataset_reqparser.add_argument(name="ds_owner_id", type=str, location="form", required=True, nullable=False)
create_dataset_reqparser.add_argument(name="ds_description", type=str, location="form", required=False, nullable=True)

update_dataset_reqparser = create_dataset_reqparser.copy()
update_dataset_reqparser.remove_argument("ds_name")

dataset_model = Model(
    "DataSet",
    {
        "ds_id": String,
        "ds_name": String,
        "ds_description": String,
        "ds_owner_id": String,
    },
)


pagination_reqparser = RequestParser(bundle_errors=True)
pagination_reqparser.add_argument("page", type=positive, required=False, default=1)
pagination_reqparser.add_argument("per_page", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

pagination_model = Model(
    "Pagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer(attribute="pages"),
        "items_per_page": Integer(attribute="per_page"),
        "total_items": Integer(attribute="total"),
        "items": List(Nested(dataset_model)),
    },
)
