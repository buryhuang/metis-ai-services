from http import HTTPStatus
from tests.util import add_dataset


def test_add_dataset(client):
    ds_name = "ds_name_FOR_TEST"
    ds_description = "ds_description_FOR_TEST"
    ds_owner_id = "ds_owner_id_FOR_TEST"
    ds_dataformat = "CSV"

    resp = add_dataset(client, ds_name, ds_description, ds_owner_id, ds_dataformat)

    assert resp.status_code == HTTPStatus.CREATED
    assert "status" in resp.json and resp.json["status"] == "success"
    assert ds_name == resp.json["ds_name"]
    assert ds_description == resp.json["ds_description"]
    # print(f"{ds_owner_id} == {resp.json['ds_description']} : {ds_description == resp.json['ds_description']}")
    # assert ds_owner_id == resp.json["ds_owner_id"]
    # assert ds_dataformat == resp.json["ds_dataformat"]
    assert resp.json["ds_id"]
