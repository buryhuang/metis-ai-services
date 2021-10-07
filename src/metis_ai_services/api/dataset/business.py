"""Business logic for /dataset API endpoints."""
from http import HTTPStatus
from uuid import uuid4
from flask import jsonify, url_for

# from flask_restx import marshal
# from metis_ai_services import db
# from metis_ai_services.api.dataset.dto import dataset_model, pagination_model
# from metis_ai_services.models.dataset import DataSet
# from metis_ai_services.models.dataframe import DataFrame

from metis_ai_services.utils.dynamodb_util import (
    add_dataset,
    get_all_datasets,
    search_datasets,
    get_dataset_by_id,
    delete_dataset_by_id,
    update_dataset_by_id,
)


def process_add_dataset(ds_params):
    ds_params["id"] = str(uuid4())

    # sqlite
    # new_ds = DataSet(**ds_dict)
    # db.session.add(new_ds)
    # db.session.commit()

    # dynamodb
    add_dataset(ds_params)

    name = ds_params["name"]
    resp = jsonify(id=ds_params["id"], status="success", message=f"New Dataset added: {name}.")
    resp.status_code = HTTPStatus.CREATED
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    return resp


# @token_required
def retrieve_dateset_list(page, per_page):
    # pagination = DataSet.query.paginate(page, per_page, error_out=False)
    # resp_data = marshal(pagination, pagination_model)
    # resp_data["links"] = _pagination_nav_links(pagination)
    # resp = jsonify(resp_data)
    # resp.headers["Link"] = _pagination_nav_header_links(pagination)
    # resp.headers["Total-Count"] = pagination.total

    # "has_prev": false,
    # "has_next": false,
    # "page": 1,
    # "total_pages": 1,
    # "items_per_page": 10,
    # "total_items": 2,
    all_datasets = get_all_datasets()
    total_items = len(all_datasets)
    total_pages = total_items // per_page + 1 if total_items % per_page > 0 else 0
    if page > total_pages:
        return jsonify([])
    else:
        print(f"total_pages:{total_pages}")
        cur_page_idx_min, cur_page_idx_max = (page - 1) * per_page, page * per_page
        items = all_datasets[cur_page_idx_min:cur_page_idx_max]
        return jsonify(
            {
                "page": page,
                "total_pages": total_pages,
                "items_per_page": per_page,
                "total_items": total_items,
                "items": items,
            }
        )


def search_datasets_by_keywords(keywords):
    # search = "%{}%".format(keywords)
    # match_dss = DataSet.query.filter(DataSet.name.like(search)).all()
    # resp = jsonify([ds.serialize for ds in match_dss])

    datasets = search_datasets(keywords)
    return jsonify(datasets)


# @token_required
def retrieve_dataset(ds_id):
    # ds_info = DataSet.query.filter_by(id=ds_id).first_or_404(description=f"{ds_id} not found in database.")
    # resp_data = marshal(ds_info, dataset_model)
    # dfs = DataFrame.query.filter_by(ds_id=ds_id).all()
    # resp_data["dataframes"] = [df.serialize for df in dfs]
    # return jsonify(resp_data)

    dataset = get_dataset_by_id(ds_id)
    return jsonify(dataset)


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
def update_dataset(ds_id, ds_params):
    # df = DataSet.query.filter_by(id=ds_id).first()
    # if df:
    #     for k, v in ds_params.items():
    #         if v:
    #             setattr(df, k, v)
    #     db.session.commit()
    #     message = f"Dataset[{ds_id}] was successfully updated"
    #     response_dict = dict(status="success", message=message)
    #     return response_dict, HTTPStatus.OK
    # return "", HTTPStatus.NOT_FOUND
    result = update_dataset_by_id(ds_id, ds_params)
    return jsonify(result)


def delete_dataset(ds_id):
    # widget = DataSet.query.filter_by(id=ds_id).first_or_404(description=f"dataset[{ds_id}] not found in database.")
    # db.session.delete(widget)
    # db.session.commit()
    # return "", HTTPStatus.NO_CONTENT
    if delete_dataset_by_id(ds_id):
        return "", HTTPStatus.OK
    return "", HTTPStatus.EXPECTATION_FAILED
