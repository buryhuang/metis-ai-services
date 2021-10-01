"""Business logic for /dataset API endpoints."""
from http import HTTPStatus
from uuid import uuid4
from flask import jsonify, url_for
from flask_restx import marshal

from metis_ai_services import db
from metis_ai_services.api.dataset.dto import pagination_model
from metis_ai_services.models.dataset import DataSet


def process_add_dataset(ds_dict):
    ds_dict["id"] = str(uuid4())
    new_ds = DataSet(**ds_dict)
    db.session.add(new_ds)
    db.session.commit()

    name = ds_dict["name"]
    resp = jsonify(id=ds_dict["id"], status="success", message=f"New Dataset added: {name}.")
    resp.status_code = HTTPStatus.CREATED
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    return resp


# @token_required
def retrieve_dataset(ds_id):
    return DataSet.query.filter_by(id=ds_id).first_or_404(description=f"{ds_id} not found in database.")


# @token_required
def retrieve_dateset_list(page, per_page):
    pagination = DataSet.query.paginate(page, per_page, error_out=False)
    resp_data = marshal(pagination, pagination_model)
    resp_data["links"] = _pagination_nav_links(pagination)
    resp = jsonify(resp_data)
    resp.headers["Link"] = _pagination_nav_header_links(pagination)
    resp.headers["Total-Count"] = pagination.total
    return resp


def search_datasets_by_keywords(keywords):
    search = "%{}%".format(keywords)
    match_dss = DataSet.query.filter(DataSet.name.like(search)).all()
    resp = jsonify([ds.serialize for ds in match_dss])
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
    widget = DataSet.query.filter_by(id=ds_id).first_or_404(description=f"{ds_id} not found in database.")
    db.session.delete(widget)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
