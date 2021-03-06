"""API endpoint definitions for /datasets namespace."""
from http import HTTPStatus
from flask_restx import Namespace, Resource
from metis_ai_services.api.dataset.business import (
    process_add_dataset,
    retrieve_dateset_list,
    # retrieve_mock_dateset_list,
    retrieve_dataset,
    update_dataset,
    delete_dataset,
    search_datasets_by_keywords,
)
from metis_ai_services.api.dataset.dto import (
    create_dataset_reqparser,
    search_dataset_reqparser,
    update_dataset_reqparser,
    pagination_reqparser,
    dataset_model,
    pagination_model,
    pagination_links_model,
)


ns_dataset = Namespace(name="datasets", validate=True)
ns_dataset.models[dataset_model.name] = dataset_model
ns_dataset.models[pagination_model.name] = pagination_model
ns_dataset.models[pagination_links_model.name] = pagination_links_model


@ns_dataset.route("", endpoint="dataset_list")
@ns_dataset.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@ns_dataset.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@ns_dataset.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class DataSetList(Resource):
    """Handles HTTP requests to URL: /datasets."""

    # @ns_dataset.doc(security="Bearer")
    @ns_dataset.response(HTTPStatus.OK, "Retrieved dataset list.", pagination_model)
    @ns_dataset.expect(pagination_reqparser)
    def get(self):
        """Retrieve a list of datasets."""
        request_data = pagination_reqparser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_dateset_list(page, per_page)

    @ns_dataset.expect(create_dataset_reqparser)
    @ns_dataset.response(int(HTTPStatus.CREATED), "New dataset was successfully created.")
    @ns_dataset.response(int(HTTPStatus.CONFLICT), "Same name dataset iis already created.")
    @ns_dataset.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataset.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def post(self):
        """create a new dataset."""
        new_ds_dict = create_dataset_reqparser.parse_args()
        return process_add_dataset(new_ds_dict)


@ns_dataset.route("/search", endpoint="ds_search")
class DataSetSearch(Resource):
    """Handles HTTP requests to URL: /datasets/search."""

    @ns_dataset.expect(search_dataset_reqparser)
    @ns_dataset.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @ns_dataset.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Interal server error.")
    def post(self):
        """query on a dataframe."""
        request_data = search_dataset_reqparser.parse_args()
        keywords = request_data.get("keywords")
        return search_datasets_by_keywords(keywords)


@ns_dataset.route("/<ds_id>", endpoint="dataset")
class DataSet(Resource):
    """Handles HTTP requests to URL: /datasets/{ds_id}."""

    # @ns_dataset.marshal_with(dataset_model)
    @ns_dataset.response(int(HTTPStatus.OK), "Retrieved dataset.", dataset_model)
    def get(self, ds_id):
        """Retrieve a dataset."""
        return retrieve_dataset(ds_id)

    @ns_dataset.response(int(HTTPStatus.OK), "Dataset was updated.", dataset_model)
    # @ns_dataset.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @ns_dataset.expect(update_dataset_reqparser)
    def put(self, ds_id):
        """Update a dataset."""
        dataset_params = update_dataset_reqparser.parse_args()
        return update_dataset(ds_id, dataset_params)

    @ns_dataset.response(int(HTTPStatus.NO_CONTENT), "Dataset was deleted.")
    @ns_dataset.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    def delete(self, ds_id):
        """Delete a dataset."""
        return delete_dataset(ds_id)
