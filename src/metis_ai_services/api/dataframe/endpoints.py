"""API endpoint definitions for /dataframes namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource
from metis_ai_services.api.dataframe.business import (
    upload_dataframe,
    retrieve_dataframe_list,
    retrieve_dataframe,
    update_dataframe,
    delete_dataframe,
    export_dataframe,
    query_dataframe,
)
from metis_ai_services.api.dataframe.dto import (
    create_dataframe_reqparser,
    update_dataset_reqparser,
    export_dataframe_reqparser,
    query_dataframe_reqparser,
    dataframe_model,
)


ns_dataframe = Namespace(name="dataframes", validate=True)
ns_dataframe.models[dataframe_model.name] = dataframe_model


@ns_dataframe.route("", endpoint="dataframe_list")
@ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@ns_dataframe.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class DataFrameList(Resource):
    """Handles HTTP requests to URL: /datasets."""

    # @ns_dataset.doc(security="Bearer")
    @ns_dataframe.response(HTTPStatus.OK, "Retrieved widget list.")
    def get(self):
        """Retrieve a list of datasets."""
        return retrieve_dataframe_list()

    @ns_dataframe.expect(create_dataframe_reqparser)
    @ns_dataframe.response(int(HTTPStatus.CREATED), "New dataset was successfully created.")
    @ns_dataframe.response(int(HTTPStatus.CONFLICT), "Same name dataset iis already created.")
    @ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def post(self):
        """create a new dataset."""
        req_data = create_dataframe_reqparser.parse_args()

        ds_id = req_data.get("ds_id")
        df_name = req_data.get("df_name")
        df_description = req_data.get("df_description")
        ds_dataformat = req_data.get("ds_dataformat")

        # TODO: validate the new dataframe attributes.

        return upload_dataframe(ds_id, df_name, df_description, ds_dataformat)


@ns_dataframe.route("/<df_id>", endpoint="dataframe")
class DataFrame(Resource):
    """Handles HTTP requests to URL: /dataframes/{ds_id}."""

    @ns_dataframe.response(int(HTTPStatus.OK), "Retrieved dataframe.", dataframe_model)
    @ns_dataframe.marshal_with(dataframe_model)
    def get(self, ds_id, df_id):
        """Retrieve a dataframe."""
        return retrieve_dataframe(ds_id, df_id)

    @ns_dataframe.response(int(HTTPStatus.OK), "Dataset was updated.", dataframe_model)
    @ns_dataframe.response(int(HTTPStatus.CREATED), "Added new widget.")
    @ns_dataframe.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @ns_dataframe.expect(update_dataset_reqparser)
    def put(self, ds_id, df_id):
        """Update a dataframe."""
        # dataset_dict = update_dataset_reqparser.parse_args()
        return update_dataframe(ds_id, df_id)

    @ns_dataframe.response(int(HTTPStatus.NO_CONTENT), "Dataset was deleted.")
    @ns_dataframe.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    def delete(self, ds_id, df_id):
        """Delete a dataframe."""
        return delete_dataframe(ds_id, df_id)


@ns_dataframe.route("/export", endpoint="df_export")
class DataFrameExport(Resource):
    """Handles HTTP requests to URL: /dataframes/export."""

    @ns_dataframe.expect(export_dataframe_reqparser)
    @ns_dataframe.response(int(HTTPStatus.CREATED), "New dataset was successfully created.")
    @ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def post(self):
        """export a dataframe."""
        export_params = export_dataframe_reqparser.parse_args()

        # TODO: export the dataframe.

        return export_dataframe(export_params)


@ns_dataframe.route("/query", endpoint="df_query")
class DataFrameQuery(Resource):
    """Handles HTTP requests to URL: /dataframes/query."""

    @ns_dataframe.expect(query_dataframe_reqparser)
    @ns_dataframe.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataframe.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def post(self):
        """query on a dataframe."""
        query_params = export_dataframe_reqparser.parse_args()

        # TODO: query on a dataframe.

        return query_dataframe(query_params)
