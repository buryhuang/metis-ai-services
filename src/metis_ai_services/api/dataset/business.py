"""Business logic for /dataset API endpoints."""
from http import HTTPStatus
from uuid import uuid4

from flask import jsonify


def process_add_dataset(ds_name: str, ds_description: str, ds_owner_id: str, ds_dataformat: str):
    # TODO: validate input parameters

    ds_new_id = str(uuid4())
    # TODO: add a new dataset model to DB

    # TODO: return appropriate response
    resp = jsonify(
        status="success",
        message="successfully create a new dataset",
        ds_id=ds_new_id,
        ds_name=ds_name,
        ds_description=ds_description,
        ds_owner_id=ds_owner_id,
        ds_dataformat=ds_dataformat,
    )

    resp.status_code = HTTPStatus.CREATED
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    return resp


# @token_required
def retrieve_dataset(ds_name):
    pass


# @token_required
def retrieve_dateset_list():
    pass


# @token_required
def update_dataset(ds_id):
    pass


def delete_dataset(ds_id):
    pass
