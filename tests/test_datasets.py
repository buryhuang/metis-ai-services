import json
import urllib3

'''local host'''
addr = 'http://127.0.0.1:5000'

def test_get_dataset():
    http = urllib3.PoolManager()
    proxies = {'https': 'http://127.0.0.1:5000'}
    r = http.request("GET", addr + "/v1/datasets?page=1&per_page=10")
    assert r.status == 200
    print(json.loads(r.data))


def test_create_get_put_del_dataset():
    http = urllib3.PoolManager()
    
    #create
    attr = {"name":"test_dataset", "description":"description", "owner_id":"owner_id", "image_url":"image_url"}
    r_create = http.request("POST", addr + "/v1/datasets", fields = attr)
    assert r_create.status == 201
    print(json.loads(r_create.data))
    id = json.loads(r_create.data)["id"]
    
    #get
    r_get = http.request("GET", addr + "/v1/datasets/" + id)
    assert r_get.status == 200
    dic = json.loads(r_get.data)
    for key in attr:
        assert attr[key] == dic[key]
    print(dic)
    
    #put
    new_attr = {"name":"test_dataset_new", "description":"description_new", "owner_id":"owner_id", "image_url":"image_url_new"}
    r_put = http.request("PUT", addr + "/v1/datasets/" + id, fields = new_attr)
    assert r_put.status == 200
    r_get = http.request("GET", addr + "/v1/datasets/" + id)
    assert r_get.status == 200
    dic = json.loads(r_get.data)
    
    for key in new_attr:
        assert new_attr[key] == dic[key]
    
    #delete
    r_delete = http.request("DELETE", addr + "/v1/datasets/" + id) 
    assert r_delete.status == 200
    print(json.loads(r_delete.data))
    
