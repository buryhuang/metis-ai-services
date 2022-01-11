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
create_dataframe_reqparser.add_argument(name="name", type=str, location="form", required=True, nullable=False)
create_dataframe_reqparser.add_argument(name="uri", type=str, location="form", required=True, nullable=False)
create_dataframe_reqparser.add_argument(name="ds_id", type=str, location="form", required=True, nullable=False)
create_dataframe_reqparser.add_argument(name="description", type=str, location="form", required=False, nullable=True)

retrieve_dataframe_reqparser = RequestParser(bundle_errors=True)
retrieve_dataframe_reqparser.add_argument(name="ds_id", type=str, location="form", required=False, nullable=True)

update_dataframe_reqparser = RequestParser(bundle_errors=True)
update_dataframe_reqparser.add_argument(name="uri", type=str, location="form", required=False, nullable=True)
update_dataframe_reqparser.add_argument(name="ds_id", type=str, location="form", required=False, nullable=True)
update_dataframe_reqparser.add_argument(name="description", type=str, location="form", required=False, nullable=True)


# TODO: export_dataframe_reqparser
export_dataframe_reqparser = RequestParser(bundle_errors=True)
# TODO: query_dataframe_reqparser
query_dataframe_reqparser = RequestParser(bundle_errors=True)
query_dataframe_reqparser.add_argument("df_id", type=str, required=True)
query_dataframe_reqparser.add_argument("select_sql_stmt", type=str, required=True)
# query_dataframe_reqparser.add_argument(name="df_id", type=str, location="form", required=True, nullable=False)
# query_dataframe_reqparser.add_argument(name="select_sql_stmt", type=str, location="form", required=True, nullable=False)


download_dataframe_reqparser = RequestParser(bundle_errors=True)
download_dataframe_reqparser.add_argument(name="df_id", type=str, location="form", required=True)
download_dataframe_reqparser.add_argument(name="select_sql_stmt", type=str, location="form", required=True)
download_dataframe_reqparser.add_argument(name="download", type=str, location="form", required=True)

dataframe_model = Model(
    "DataFrame",
    {"id": String, "name": String, "uri": String, "ds_id": String, "description": String},
)
