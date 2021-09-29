import io
import boto3
import pandas as pd
import pandasql as pdsql


def get_s3_df():
    AWS_ACCESS_KEY_ID = "AKIAQWNS2AWMWMXEPS3Q"
    AWS_SECRET_ACCESS_KEY = "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"
    # s3://meitisa-api-data/police_killings.csv
    AWS_S3_BUCKET = "meitisa-api-data"
    s3_key = "police_killings.csv"
    s3_client = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3_obj = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=s3_key)
    status = s3_obj.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        df = pd.read_csv(io.BytesIO(s3_obj["Body"].read()), encoding="ISO-8859-1")
        df.fillna("", inplace=True)
        return df

    return None


def exec_select_stmt(select_sql_stmt):
    df = get_s3_df()
    result = pdsql.sqldf(select_sql_stmt)
    return result.to_json(orient="records")
