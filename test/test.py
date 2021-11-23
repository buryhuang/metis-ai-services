import requests


with requests.get("https://app.metis-ai.com/v1/datasets", params={'page':1, 'per_page':10}) as resp:
    print(resp.status_code)
    print(resp.text)


# 2494d19b-369e-4b2a-9a25-74320cb7997c