import boto3
import hashlib
from boto3.dynamodb.conditions import Key, Attr

# from metis_ai_services.api import dataframe

DataSet_TN = "DataSet"
DataFrame_TN = "DataFrame"
User_TN = "User"
UserSession_TN = "UserSession"

AWS_ACCESS_KEY_ID = "AKIAQWNS2AWMWMXEPS3Q"
AWS_SECRET_ACCESS_KEY = "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"


def get_dynamodb_client():
    dynamodb = None
    try:
        dynamodb = boto3.client(
            "dynamodb",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        return dynamodb
    except Exception as e:
        print(e)
    return dynamodb


def get_dynamodb_resource():
    dynamodb = None
    try:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        return dynamodb
    except Exception as e:
        print(e)
    return dynamodb


def init_dynamo_db():
    try:
        dynamodb = get_dynamodb_client()
        if dynamodb:
            existing_tables = dynamodb.list_tables()["TableNames"]
            # print(f"existing_tables: {existing_tables}")
            # for existing_table in existing_tables:
            #     print(existing_table)

            if DataSet_TN not in existing_tables:
                _create_dataset_tbl(dynamodb)
            if DataFrame_TN not in existing_tables:
                _create_dataframe_tbl(dynamodb)
            if User_TN not in existing_tables:
                _create_user_tbl(dynamodb)
            if UserSession_TN not in existing_tables:
                _create_user_session_tbl(dynamodb)
    except Exception as e:
        print(e)


def _create_dataset_tbl(dynamodb):
    dynamodb.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S",
            },
            {
                "AttributeName": "owner_id",
                "AttributeType": "S",
            },
        ],
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH",
            },
            {
                "AttributeName": "owner_id",
                "KeyType": "RANGE",
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
        TableName=DataSet_TN,
    )


def _create_dataframe_tbl(dynamodb):
    dynamodb.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S",
            }
        ],
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH",
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
        TableName=DataFrame_TN,
    )


def _create_user_tbl(dynamodb):
    dynamodb.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "email",
                "AttributeType": "S",
            }
        ],
        KeySchema=[
            {
                "AttributeName": "email",
                "KeyType": "HASH",
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
        TableName=User_TN,
    )


def _create_user_session_tbl(dynamodb):
    dynamodb.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "token",
                "AttributeType": "B",
            }
        ],
        KeySchema=[
            {
                "AttributeName": "token",
                "KeyType": "HASH",
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
        TableName=UserSession_TN,
    )


def find_user(email):
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(User_TN)
        resp = table.query(KeyConditionExpression=Key("email").eq(email))
        print(f"find_user:{resp}")
        if len(resp["Items"]) == 1:
            return resp["Items"][0]
    except Exception as e:
        print(e)
    return None


def check_password(email, password):
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(User_TN)
        resp = table.query(KeyConditionExpression=Key("email").eq(email))
        if len(resp["Items"]) == 0:
            return False
        user_info = resp["Items"][0]
        print(f"check_password:{user_info}")
        if user_info["password"] == hashlib.pbkdf2_hmac("sha256", str.encode(password), b"salt", 100000).hex():
            return True
    except Exception as e:
        print(e)
    return False


def register_user(email, password, name, user_public_id, message):
    result = {"status": "failed", "msg": ""}
    print(password)
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(User_TN)
        if not find_user(email):
            table.put_item(
                Item={
                    "email": email,
                    "name": name,
                    "password": hashlib.pbkdf2_hmac("sha256", str.encode(password), b"salt", 100000).hex(),
                    "public_id": user_public_id,
                    "message": message,
                }
            )
            result["status"] = "success"
            result["msg"] = f"User({email}) have been added."
        else:
            result["msg"] = f"User({email}) exists."
    except Exception as e:
        result["msg"] = str(e)

    return result


def add_token(token):
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(UserSession_TN)
        table.delete_item(Key={"token": token})
        resp = table.put_item(Item={"token": token})
        if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True
    except Exception as e:
        print(e)
    return False


def check_token(token):
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(UserSession_TN)
        resp = table.query(KeyConditionExpression=Key("token").eq(str.encode(token)))
        if len(resp["Items"]) > 0:
            return True
    except Exception as e:
        print(f"check_token:{e}")
    return False


def remove_token(token):
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(UserSession_TN)
        table.delete_item(Key={"token": str.encode(token)})
    except Exception as e:
        print(f"remove_token:{e}")


def add_dataframe(df_params):
    result = {"status": "failed", "msg": ""}
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataFrame_TN)
        df_name = df_params["name"]
        resp = table.scan(FilterExpression=Attr("name").eq(df_name))
        if len(resp["Items"]) == 0:
            table.put_item(Item=df_params)
            result["status"] = "success"
            result["msg"] = f"dataframe({df_params['id']}) have been added."
        else:
            result["msg"] = f"dataframe(name='{df_name}') exists."
    except Exception as e:
        result["msg"] = str(e)

    return result


def get_all_dataframes():
    dataframes = []
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataFrame_TN)
        resp = table.scan()
        dataframes = resp["Items"]
    except Exception as e:
        print(e)
    return dataframes


def delete_dataframe_by_id(df_id):
    result = {"status": "failed", "msg": ""}
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataFrame_TN)
        resp = table.query(KeyConditionExpression=Key("id").eq(df_id))
        if len(resp["Items"]) > 0:
            df = resp["Items"][0]
            resp = table.delete_item(Key={"id": df["id"]})
            result["status"] = "success"
            result["msg"] = f"dataframe({df_id}) has been deleted."
        else:
            result["msg"] = f"dataframe({df_id}) not founded."
    except Exception as e:
        result["msg"] = str(e)
    return result


def get_dataframe_by_id(df_id):
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataFrame_TN)
        resp = table.query(KeyConditionExpression=Key("id").eq(df_id))
        if len(resp["Items"]) > 0:
            df = resp["Items"][0]
            return df
    except Exception as e:
        print(e)
    return None


def get_dataframe_by_dsid(ds_id):
    dfs = None
    dynamodb = get_dynamodb_resource()
    try:
        if dynamodb:
            table = dynamodb.Table(DataFrame_TN)
            if table:
                resp = table.scan(FilterExpression=Attr("ds_id").eq(ds_id))
                dfs = resp["Items"]
    except Exception as e:
        print(e)
    return dfs


def update_dataframe_by_id(df_id, df_params):
    result = {"status": "", "msg": ""}
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataFrame_TN)
        resp = table.query(KeyConditionExpression=Key("id").eq(df_id))
        if len(resp["Items"]) > 0:
            df = resp["Items"][0]
            for k, v in df_params.items():
                if v:
                    df[k] = v
            table.put_item(Item=df)
            result["status"] = "success"
            result["msg"] = f"dataframe({df_id}) has been updated."
        else:
            result["status"] = "failed"
            result["msg"] = f"dataframe({df_id}) not founded."
    except Exception as e:
        result["status"] = "failed"
        result["msg"] = str(e)
    return result


def add_dataset(ds_params):
    dynamodb = get_dynamodb_client()
    if dynamodb:
        try:
            resp = dynamodb.put_item(
                TableName=DataSet_TN,
                Item={
                    "id": {"S": ds_params["id"]},
                    "owner_id": {"S": ds_params["owner_id"]},
                    "name": {"S": ds_params["name"]},
                    "description": {"S": ds_params["description"]},
                    "image_url": {"S": ds_params["image_url"]},
                },
            )
            print(resp)
        except Exception as e:
            print(e)


def get_all_datasets():
    datasets = []
    dynamodb = get_dynamodb_resource()
    try:
        if dynamodb:
            table = dynamodb.Table(DataSet_TN)
            if table:
                resp = table.scan()
                datasets = resp["Items"]
    except Exception as e:
        print(e)
    return datasets


def search_datasets(keywords):
    datasets = []
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataSet_TN)
        resp = table.scan(FilterExpression=Attr("name").contains(keywords) | Attr("description").contains(keywords))
        datasets = resp["Items"]
    except Exception as e:
        print(e)
    return datasets


def get_dataset_by_id(ds_id):
    dataset = None
    dynamodb = get_dynamodb_resource()
    try:
        if dynamodb:
            table = dynamodb.Table(DataSet_TN)
            if table:
                resp = table.query(KeyConditionExpression=Key("id").eq(ds_id))
                dataset = resp["Items"][0]
    except Exception as e:
        print(e)
    return dataset


def delete_dataset_by_id(ds_id):
    deleted = False
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataSet_TN)
        resp = table.query(KeyConditionExpression=Key("id").eq(ds_id))
        if len(resp["Items"]) > 0:
            dataset = resp["Items"][0]
            resp = table.delete_item(Key={"id": dataset["id"], "owner_id": dataset["owner_id"]})
            deleted = True
    except Exception as e:
        print(e)
    return deleted


def update_dataset_by_id(ds_id, ds_params):
    result = {"status": "", "msg": ""}
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(DataSet_TN)
        resp = table.query(KeyConditionExpression=Key("id").eq(ds_id))
        if len(resp["Items"]) > 0:
            dataset = resp["Items"][0]
            for k, v in ds_params.items():
                if v:
                    dataset[k] = v
            table.put_item(Item=dataset)
            result["status"] = "success"
            result["msg"] = f"dataset({ds_id}) has been updated."
        else:
            result["status"] = "failed"
            result["msg"] = f"dataset({ds_id}) not founded."
    except Exception as e:
        result["status"] = "failed"
        result["msg"] = str(e)
    return result
