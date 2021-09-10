"""Business logic for /dataset API endpoints."""
from http import HTTPStatus
from uuid import uuid4
from flask import jsonify, url_for
from flask_restx import marshal

from metis_ai_services.api.dataset.dto import pagination_model
from metis_ai_services.models.dataset import DataSet


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
def retrieve_dateset_list(page, per_page):
    pagination = DataSet.query.paginate(page, per_page, error_out=False)
    resp_data = marshal(pagination, pagination_model)
    resp_data["links"] = _pagination_nav_links(pagination)
    resp = jsonify(resp_data)
    resp.headers["Link"] = _pagination_nav_header_links(pagination)
    resp.headers["Total-Count"] = pagination.total
    return resp


def _pagination_nav_links(pagination):
    nav_links = {}
    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages
    nav_links["self"] = url_for("api.dataset_list", page=this_page, per_page=per_page)
    nav_links["first"] = url_for("api.dataset_list", page=1, per_page=per_page)
    if pagination.has_prev:
        nav_links["prev"] = url_for("api.dataset_list", page=this_page - 1, per_page=per_page)
    if pagination.has_next:
        nav_links["next"] = url_for("api.dataset_list", page=this_page + 1, per_page=per_page)
    nav_links["last"] = url_for("api.dataset_list", page=last_page, per_page=per_page)
    return nav_links


def _pagination_nav_header_links(pagination):
    url_dict = _pagination_nav_links(pagination)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")


# @token_required
def update_dataset(ds_id):
    pass


def delete_dataset(ds_id):
    pass
