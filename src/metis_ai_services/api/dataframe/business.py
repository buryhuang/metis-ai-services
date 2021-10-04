"""Business logic for /dataset API endpoints."""
from http import HTTPStatus
from uuid import uuid4

from flask import jsonify

from metis_ai_services import db
from metis_ai_services.models.dataframe import DataFrame
from metis_ai_services.utils.s3_util import exec_select_stmt


def process_add_dataframe(df_dict):
    df_dict["id"] = str(uuid4())
    new_df = DataFrame(**df_dict)
    db.session.add(new_df)
    db.session.commit()

    name = df_dict["name"]
    resp = jsonify(id=df_dict["id"], status="success", message=f"New DataFrame added: {name}.")
    resp.status_code = HTTPStatus.CREATED
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    return resp


# @token_required
def retrieve_dataframe_list():
    dfs = DataFrame.query.all()
    resp = jsonify([df.serialize for df in dfs])
    return resp


# @token_required
def retrieve_dataframe(df_id):
    return DataFrame.query.filter_by(id=df_id).first_or_404(description=f"DataFrame[ID:{df_id}] not found in database.")


# @token_required
def update_dataframe(df_id, df_params):
    msg = ""
    try:
        df = DataFrame.query.filter_by(id=df_id).first()
        if df:
            if df_params["uri"] is not None:
                df.uri = df_params["uri"]
            if df_params["ds_id"] is not None:
                df.ds_id = df_params["ds_id"]
            if df_params["description"] is not None:
                df.description = df_params["description"]
            db.session.commit()
            msg = f"dataframe[{df_id}] was updated."
        else:
            msg = f"dataframe[{df_id}] was not found."
    except Exception as e:
        msg = f"{e}"
    return jsonify({"message": msg})


def delete_dataframe(df_id):
    msg = ""
    try:
        df = DataFrame.query.filter_by(id=df_id).first()
        if df:
            db.session.delete(df)
            db.session.commit()
            msg = f"dataframe[{df_id}] was deleted."
        else:
            msg = f"dataframe[{df_id}] was not found."
        return jsonify({"message": msg})
    except Exception as e:
        msg = f"{e}"


def export_dataframe(export_params):
    pass


def query_dataframe(df_id, select_sql_stmt):
    df = DataFrame.query.filter_by(id=df_id).first()
    if df is not None:
        return exec_select_stmt(df.uri, select_sql_stmt)
    return jsonify({"message": f"DataFrame[ID:{df_id}] not found in database."})
