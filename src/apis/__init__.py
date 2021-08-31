from flask_restx import Api

from .dataframe import ns_dataframes, ns_dataframe
from .datasets import ns_datasets, ns_dataset

api = Api(title="MetisAI API", version="0.1.0", description="MetisAI APIs",)

api.add_namespace(ns_datasets, path='/datasets')
api.add_namespace(ns_dataset, path='/dataset')

api.add_namespace(ns_dataframes, path='/dataframes')
api.add_namespace(ns_dataframe, path='/dataframe')
