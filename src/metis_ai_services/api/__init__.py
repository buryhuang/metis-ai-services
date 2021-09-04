"""API blueprint configuration."""
from flask import Blueprint
from flask_restx import Api

from metis_ai_services.api.auth.endpoints import auth_ns
from metis_ai_services.api.widgets.endpoints import widget_ns

from metis_ai_services.api.dataframe import ns_dataframes, ns_dataframe
from metis_ai_services.api.datasets import ns_datasets, ns_dataset

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    version="1.0",
    title="Flask API with JWT-Based Authentication",
    description="Welcome to the Swagger UI documentation site!",
    doc="/ui",
    authorizations=authorizations,
)

# api = Api(
#     title="MetisAI API",
#     version="0.1.0",
#     description="MetisAI APIs",
# )

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(widget_ns, path="/wigdet")

api.add_namespace(ns_datasets, path="/datasets")
api.add_namespace(ns_dataset, path="/dataset")

api.add_namespace(ns_dataframes, path="/dataframes")
api.add_namespace(ns_dataframe, path="/dataframe")
