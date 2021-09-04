from flask_restx import Namespace, Resource

# endpoint: http(s)://[xxx-domain].metisai.com/datasets
ns_datasets = Namespace(
    "datasets", description="Custom or Trails datasets that provided by MetisAI."
)


# endpoint: http(s)://[xxx-domain].metisai.com/dataset
ns_dataset = Namespace("dataset", description="Individual dataset RESTFul APIs")


default_datasets = [
    "cypto",
    "covid",
    "realestate",
    "socialnetworkrelations",
    "sports",
    "socialissues",
]


@ns_datasets.route("/")
class DataSetsRes(Resource):
    """The Endpoint for the tables that user upload to MetiasAI Data Platform"""

    def get(self):
        """This gets list of all trails datasets

        Returns:
            list: All trails datasets in MetisAI.
                  Example: ['cypto', 'covid', 'realestate', 'socialnetworkrelations', 'sports',
                            'socialissues', ...]
        """
        return default_datasets

    def post(self):
        """This creates a new dataset"""
        pass


@ns_dataset.route("/<string:dataset_id>")
class DataSetRes(Resource):
    """[summary]

    Args:
        Resource ([type]): [description]
    """

    def get(self, dataset_id):
        """Get a DataSet

        Args:
            dataset_id ([type]): [description]
        """
        pass

    def put(self, dataset_id):
        """Update a DataSet

        Args:
            dataset_id ([type]): [description]
        """
        pass

    def delete(self, dataset_id):
        """Delete a DataSet

        Args:
            dataset_id ([type]): [description]
        """
        pass
