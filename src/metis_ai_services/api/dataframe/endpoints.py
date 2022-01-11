"""API endpoint definitions for /dataframes namespace."""
from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from io import StringIO
import csv
from flask import make_response
from metis_ai_services.api.dataframe.business import (
    process_add_dataframe,
    retrieve_dataframe_list,
    retrieve_dataframe,
    update_dataframe,
    delete_dataframe,
    # export_dataframe,
    query_dataframe,
    download_dataframe,
)
from metis_ai_services.api.dataframe.dto import (
    create_dataframe_reqparser,
    # retrieve_dataframe_reqparser,
    update_dataframe_reqparser,
    # export_dataframe_reqparser,
    query_dataframe_reqparser,
    download_dataframe_reqparser,
    dataframe_model,
)


ns_dataframe = Namespace(name="dataframes", validate=True)
ns_dataframe.models[dataframe_model.name] = dataframe_model


@ns_dataframe.route("", endpoint="dataframe_list")
@ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@ns_dataframe.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class DataFrameList(Resource):
    """Handles HTTP requests to URL: /dataframes."""

    # @ns_dataset.doc(security="Bearer")
    @ns_dataframe.response(HTTPStatus.OK, "Retrieved dataframe list.")
    def get(self):
        """Retrieve a list of dataframes."""
        return retrieve_dataframe_list()

    @ns_dataframe.expect(create_dataframe_reqparser)
    @ns_dataframe.response(int(HTTPStatus.CREATED), "New dataframe was successfully created.")
    @ns_dataframe.response(int(HTTPStatus.CONFLICT), "Same name dataframe is already created.")
    @ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def post(self):
        """create a new dataframe."""
        new_df_dict = create_dataframe_reqparser.parse_args()
        return process_add_dataframe(new_df_dict)


@ns_dataframe.route("/<df_id>", endpoint="dataframe")
class DataFrame(Resource):
    """Handles HTTP requests to URL: /dataframes/{df_id}."""

    @ns_dataframe.response(int(HTTPStatus.OK), "Retrieved dataframe.", dataframe_model)
    # @ns_dataframe.marshal_with(dataframe_model)
    def get(self, df_id):
        """Retrieve a dataframe."""
        df = retrieve_dataframe(df_id)
        if df:
            return jsonify(df)
        else:
            return "", HTTPStatus.NOT_FOUND

    # @ns_dataframe.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    # @ns_dataframe.response(int(HTTPStatus.OK), "Dataframe was updated.", dataframe_model)
    # @ns_dataframe.response(int(HTTPStatus.CREATED), "Added new widget.")
    @ns_dataframe.expect(update_dataframe_reqparser)
    def put(self, df_id):
        """Update a dataframe."""
        df_params = update_dataframe_reqparser.parse_args()
        return update_dataframe(df_id, df_params)

    # @ns_dataframe.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @ns_dataframe.response(int(HTTPStatus.NO_CONTENT), "Dataframe was deleted.")
    def delete(self, df_id):
        """Delete a dataframe."""
        return delete_dataframe(df_id)


# @ns_dataframe.route("/export", endpoint="df_export")
# class DataFrameExport(Resource):
#     """Handles HTTP requests to URL: /dataframes/export."""

#     @ns_dataframe.expect(export_dataframe_reqparser)
#     @ns_dataframe.response(int(HTTPStatus.CREATED), "New dataframe was successfully created.")
#     @ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
#     @ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
#     def post(self):
#         """export a dataframe."""
#         export_params = export_dataframe_reqparser.parse_args()

#         # TODO: export the dataframe.

#         return export_dataframe(export_params)


@ns_dataframe.route("/query", endpoint="df_query")
class DataFrameQuery(Resource):
    """Handles HTTP requests to URL: /dataframes/query."""

    @ns_dataframe.expect(query_dataframe_reqparser)
    @ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def get(self):
        """query on a dataframe."""
        request_data = query_dataframe_reqparser.parse_args()
        df_id = request_data.get("df_id")
        select_sql_stmt = request_data.get("select_sql_stmt")
        return query_dataframe(df_id, select_sql_stmt)

@ns_dataframe.route("/download", endpoint = "df_download")
class DataFrameDownload(Resource):
    @ns_dataframe.expect(download_dataframe_reqparser)
    @ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def post(self):
        request_data = download_dataframe_reqparser.parse_args()
        df_id = request_data.get("df_id")
        select_sql_stmt = request_data.get("select_sql_stmt")
        download = request_data.get("download")
        if int(download) == 1:
            query_result = download_dataframe(df_id, select_sql_stmt)
            si = StringIO()
            cw = csv.writer(si)
            cw.writerows(query_result)
            response = make_response(si.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=download.csv"
            response.headers["Content-type"] = "text/csv"
            return response
        else:
            return HTTPStatus.OK




