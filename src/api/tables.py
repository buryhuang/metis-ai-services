from flask import Flask, request
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


user_raw_tables = {
    "user_001":['tbl_001'],
    "user_003":['tbl_002'],
    "user_002":['tbl_003'],
}

### endpoint: http(s)://[xxx-domain].metisai.com/rawtables
ns_rawtable = api.namespace('rawtables', description='The tables that user upload to MetiasAI Data Platform')
@ns_rawtable.route('/')
class RawTables(Resource):
    """ The Endpoint for the tables that user upload to MetiasAI Data Platform
    """
    
    def get(self, user_id):
        """ Get all tables belongs to <user_id>

        Args:
            user_id (string): [description]

        Returns:
            list: The table names(or alias) belongs to current user.
                  Example: ['tbl_001', 'tbl_xyz', 'tbl_!@#']
        """        
        cur_user_tables = []
        if user_id in user_raw_tables:
            cur_user_tables = user_raw_tables[user_id]
        return cur_user_tables
    
    def post(self, user_id, raw_table_name):
        """ add a new raw table

        Args:
            user_id (string): User ID
            raw_table_name (string): a new raw table name

        Returns:
            [type]: [description]
        """
        # TODO:
        # Case 01 -  user DO NOT exits
        # Case 02 -  duplicated table name
        if user_id in user_raw_tables:
            user_raw_tables[user_id].append(raw_table_name)
        else:
            user_raw_tables[user_id] = [raw_table_name]

        return {'msg': "ok"}


### endpoint: http(s)://[xxx-domain].metisai.com/rawtable
ns_rawtable = api.namespace('rawtable', description='individual raw table RESTFul Services')
@ns_rawtable.route('/<string:rawtable_id>')
class RawTableResource(Resource):
    """[summary]

    Args:
        Resource ([type]): [description]
    """    
    def get(self, rawtable_id):
        """[summary]

        Args:
            rawtable_id ([type]): [description]
        """        
        pass

    def put(self, rawtable_id):
        """[summary]

        Args:
            rawtable_id ([type]): [description]
        """        
        pass

    def delete(self, rawtable_id):
        """[summary]

        Args:
            rawtable_id ([type]): [description]
        """        
        pass

    
    

if __name__ == '__main__':
    app.run(debug=True)