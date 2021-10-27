"""Business logic for /dataset API endpoints."""
from http import HTTPStatus
from uuid import uuid4
from flask import jsonify

# from metis_ai_services import db
# from metis_ai_services.models.dataframe import DataFrame
from metis_ai_services.utils.s3_util import exec_select_stmt
from metis_ai_services.utils.dynamodb_util import (
    add_dataframe,
    get_all_dataframes,
    delete_dataframe_by_id,
    get_dataframe_by_id,
    update_dataframe_by_id,
)


def process_add_dataframe(df_params):
    df_params["id"] = str(uuid4())

    # sqlite
    # new_df = DataFrame(**df_dict)
    # db.session.add(new_df)
    # db.session.commit()

    # dynamodb
    result = add_dataframe(df_params)
    resp = jsonify(result)

    # name = df_params["name"]
    # resp = jsonify(id=df_params["id"], status="success", message=f"New DataFrame added: {name}.")
    # resp.status_code = HTTPStatus.CREATED
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    return resp


# @token_required
def retrieve_dataframe_list():
    # dfs = DataFrame.query.all()
    # resp = jsonify([df.serialize for df in dfs])
    # return resp
    return get_all_dataframes()


# @token_required
def retrieve_dataframe(df_id):
    # return DataFrame.query.filter_by(id=df_id).first_or_404(
    #   description=f"DataFrame[ID:{df_id}] not found in database."
    # )
    df = get_dataframe_by_id(df_id)
    return df


# @token_required
def update_dataframe(df_id, df_params):
    # df = DataFrame.query.filter_by(id=df_id).first()
    # if df:
    #     for k, v in df_params.items():
    #         if v:
    #             setattr(df, k, v)
    #     db.session.commit()
    #     message = f"Dataframe[{df_id}] was successfully updated"
    #     response_dict = dict(status="success", message=message)
    #     return response_dict, HTTPStatus.OK
    # return "", HTTPStatus.NOT_FOUND
    result = update_dataframe_by_id(df_id, df_params)
    return jsonify(result)


def delete_dataframe(df_id):
    # df = DataFrame.query.filter_by(id=df_id).first_or_404(description=f"dataframe[{df_id}] not found in database.")
    # db.session.delete(df)
    # db.session.commit()
    # return "", HTTPStatus.NO_CONTENT

    result = delete_dataframe_by_id(df_id)
    return jsonify(result)


def export_dataframe(export_params):
    pass


def query_dataframe(df_id, select_sql_stmt):
    # df = DataFrame.query.filter_by(id=df_id).first()
    # if df is not None:
    #     return exec_select_stmt(df.uri, select_sql_stmt)
    # return jsonify({"message": f"DataFrame[ID:{df_id}] not found in database."})
    df = get_dataframe_by_id(df_id)
    if df is not None:
        return exec_select_stmt(df["name"], df["uri"], select_sql_stmt)
    return jsonify({"message": f"DataFrame[ID:{df_id}] not found in database."})
