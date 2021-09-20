"""Business logic for /dataset API endpoints."""
import random
from http import HTTPStatus
from uuid import uuid4
from flask import jsonify, url_for
from flask_restx import marshal

from metis_ai_services.api.dataset.dto import pagination_model, dataset_model
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


def retrieve_mock_dateset_list():
    mock_datasets = [
        {
            "ds_id": str(uuid4()),
            "ds_name": "Amazon.com, Inc. (AMZN)",
            "ds_description": "Stock Price of Amazon.com from Sep 1 1997 to Sep 1 2021.",
            "ds_files": random.randint(1, 12),
            "ds_usability": random.randint(1, 10240),
            "ds_owner_id": "metisai",
            "ds_init_timestamp": "09/11/2021 06:07:08",
        },
        {
            "ds_id": str(uuid4()),
            "ds_name": "2021 Olympic in Toyko",
            "ds_description": "Data about Athletes, Teams, Coaches, Events.",
            "ds_files": random.randint(1, 12),
            "ds_usability": random.randint(1, 10240),
            "ds_owner_id": "metisai",
            "ds_init_timestamp": "09/11/2021 06:07:08",
        },
        {
            "ds_id": str(uuid4()),
            "ds_name": "Red Wine Quality",
            "ds_description": "Simple and clean practice dataset for regression",
            "ds_files": random.randint(1, 12),
            "ds_usability": random.randint(1, 10240),
            "ds_owner_id": "metisai",
            "ds_init_timestamp": "09/11/2021 06:07:08",
        },
        {
            "ds_id": str(uuid4()),
            "ds_name": "Bitcoin tweets - 16M tweets",
            "ds_description": "Market Based Sentiment Assignment with Stock Data",
            "ds_files": random.randint(1, 12),
            "ds_usability": random.randint(1, 10240),
            "ds_owner_id": "metisai",
            "ds_init_timestamp": "09/11/2021 06:07:08",
        },
        {
            "ds_id": str(uuid4()),
            "ds_name": "Google Play Store Apps",
            "ds_description": "Web scraped data of 10k Play Store apps.",
            "ds_files": random.randint(1, 12),
            "ds_usability": random.randint(1, 10240),
            "ds_owner_id": "metisai",
            "ds_init_timestamp": "09/11/2021 06:07:08",
        },
    ]
    resp_data = marshal(mock_datasets, dataset_model)
    resp = jsonify(resp_data)
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
