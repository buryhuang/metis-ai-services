from flask_restx import Namespace, Resource, fields


ns_dataframes = Namespace("dataframes", description="DataFrames in specific DataSet")
ns_dataframe = Namespace("dataframe", description="Individual DataFrame RESTFul Services")
Model_DataFrame = ns_dataframe.model(
    "mdl_DataFrame",
    {
        "dataframe_id": fields.String(Required=True, description=""),
        "dataframe_name": fields.String(Required=True, description=""),
        "dataset_id": fields.String(Required=True, description=""),
        "location": fields.String(Required=True, description=""),
        "user_id": fields.String(Required=False, description=""),
    },
)

# TODO: /dataset/{dataset_id}/dataframes


# endpoint: http(s)://[xxx-domain].metisai.com/dataframes
@ns_dataframes.route("/<string:dataset_id>")
class DataFramesRes(Resource):

    # @ns_dataframes.doc('list_dataframes')
    @ns_dataframes.marshal_list_with(Model_DataFrame)
    def get(self):
        """List all dataframes belongs to current dataset

        Returns:
            [type]: [description]
        """
        default_dataframes = []
        # TODO: init dataframes belongs to current dataset
        # ...
        return default_dataframes

    @ns_dataframes.marshal_with(Model_DataFrame)
    def post(self):
        """Create a DataFrame"""
        # TODO:
        # Case 01 -  user DO NOT exits
        # Case 02 -  duplicated table name
        pass


##################################################################################################
##################################################################################################


# endpoint: http(s)://[xxx-domain].metisai.com/dataframe
@ns_dataframe.route("/<string:dataframe_id>")
class DataFrameRes(Resource):
    """[summary]

    Args:
        Resource ([type]): [description]
    """

    def get(self, dataframe_id):
        """Get a DataFrame

        Args:
            dataframe_id ([type]): [description]
        """
        pass

    def put(self, dataframe_id):
        """Update a DataFrame

        Args:
            dataframe_id ([type]): [description]
        """
        pass

    def patch(self, dataframe_id):
        """Update a DataFrame with one or more specific attributes

        Args:
            dataframe_id ([type]): [description]
        """
        pass

    def delete(self, dataframe_id):
        """Delete a DataFrame

        Args:
            dataframe_id ([type]): [description]
        """
        pass
