"""Business logic for /dataset API endpoints."""
from http import HTTPStatus
from uuid import uuid4

from flask import jsonify


def upload_dataframe(ds_id: str, df_name: str, df_description: str, df_dataformat: str):
    # TODO: validate input parameters

    df_new_id = str(uuid4())
    # TODO: add a new dataframe

    # TODO: return appropriate response
    resp = jsonify(
        status="success",
        message="successfully create a new dataset",
        ds_id=ds_id,
        df_id=df_new_id,
        df_name=df_name,
        df_description=df_description,
        ds_dataformat=df_dataformat,
    )

    resp.status_code = HTTPStatus.CREATED
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    return resp


# @token_required
def retrieve_dataframe_list():
    pass


# @token_required
def retrieve_dataframe(ds_id, df_id):
    pass


# @token_required
def update_dataframe(ds_id, df_id):
    pass


def delete_dataframe(ds_id, df_id):
    pass


def export_dataframe(export_params):
    pass


def query_dataframe(export_params):
    pass
