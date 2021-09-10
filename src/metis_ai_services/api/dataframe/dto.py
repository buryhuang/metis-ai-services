"""Parsers and serializers for /dataframes API endpoints."""
import re

from flask_restx import Model
from flask_restx.fields import String
from flask_restx.reqparse import RequestParser


def validate_name(name):
    """Validation method for a string containing only letters, numbers, '-' and '_'."""
    if not re.compile(r"^[\w-]+$").match(name):
        raise ValueError(
            f"'{name}' contains one or more invalid characters. Widget name must "
            "contain only letters, numbers, hyphen and underscore characters."
        )
    return name


# bundle_errors=True: all error messages reported for all arguments in our request parser.
create_dataframe_reqparser = RequestParser(bundle_errors=True)
# Add Argument Ref.
create_dataframe_reqparser.add_argument(name="df_id", type=str, location="form", required=True, nullable=False)
create_dataframe_reqparser.add_argument(name="df_name", type=str, location="form", required=True, nullable=False)
create_dataframe_reqparser.add_argument(name="df_uri", type=str, location="form", required=True, nullable=False)
create_dataframe_reqparser.add_argument(name="ds_id", type=str, location="form", required=True, nullable=False)
create_dataframe_reqparser.add_argument(name="df_description", type=str, location="form", required=False, nullable=True)
create_dataframe_reqparser.add_argument(name="df_dataformat", type=str, location="form", required=False, nullable=True)

update_dataset_reqparser = create_dataframe_reqparser.copy()
update_dataset_reqparser.remove_argument("df_name")


# TODO: export_dataframe_reqparser
export_dataframe_reqparser = RequestParser(bundle_errors=True)
# TODO: query_dataframe_reqparser
query_dataframe_reqparser = RequestParser(bundle_errors=True)

dataframe_model = Model(
    "DataFrame",
    {
        "df_id": String,
        "df_name": String,
        "df_uri": String,
        "ds_id": String,
        "df_description": String,
        "df_dataformat": String,
    },
)
