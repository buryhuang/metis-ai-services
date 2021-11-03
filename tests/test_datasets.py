import json
import urllib3


def test_get_dataset():
    http = urllib3.PoolManager()
    r = http.request("GET", "https://api.metis-ai.com/v1/datasets?page=1&per_page=10")
    assert r.status == 200
    print(json.loads(r.data)["items"])


def test_create_del_dataset():
    pass
    # http = urllib3.PoolManager()
    # r = http.request('POST', 'https://api.metis-ai.com/v1/datasets',
    #                  fields={
    #                      "name": "YYYY",
    #                      "description": "YYYY",
    #                      "owner_id": "admin",
    #                      "image_url": "url",
    #                  })
    # print(r.status)
    # print(json.loads(r.data))

    # r = http.request('DELETE', 'https://api.metis-ai.com/v1/datasets/c7f575de-9e79-4702-8385-d471c7dcc430')
    # print(r.status)
