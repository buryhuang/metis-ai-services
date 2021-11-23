import requests

# for git flow


def test_get_dataframes():
    response = requests.get("https://api.metis-ai.com/v1/dataframes")
    assert response.status_code == 200
    response_body = response.json()
    assert response.headers["Content-Type"] == "application/json"
    assert len(response_body) == 3


def test_get_dataframes_by_df_id():
    response = requests.get(
        "https://api.metis-ai.com/v1/dataframes/e4786a01-35d2-4111-8d5f-9664d72e9c97")
    assert response.status_code == 200


def test_post_dataframes():
    response = requests.post("https://api.metis-ai.com/v1/dataframes", data={
                             'name': "police-killing-df", 'uri': "s3://metisai-api-data/police_killings.csv", 'ds_id': "4ef6785d-cbf9-4c87-bdf6-23c9b6f044d6", 'description': "dxxxxxx"})
    assert response.status_code == 200


def test_put_dataframes_by_df_id():
    response = requests.put(
        "https://api.metis-ai.com/v1/dataframes/32b6bbc7-60f1-42fd-9db4-7b668b60c305", data={
            'name': "police-killing-df", 'uri': "s3://metisai-api-data/police_killings.csv", 'ds_id': "4ef6785d-cbf9-4c87-bdf6-23c9b6f044d6", 'description': "dxxxxxx"})
    assert response.status_code == 200


def test_delete_dataframes_by_df_id():
    response = requests.delete(
        "https://api.metis-ai.com/v1/dataframes/32b6bbc7-60f1-42fd-9db4-7b668b60c305")
    assert response.status_code == 200
