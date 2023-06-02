import requests


def read_kv(account_id: str, api_key: str, namespace_id: str, key: str) -> str:
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    r = requests.get(url, headers=headers)
    return r.text


def set_kv(account_id: str, api_key: str, namespace_id: str, key: str, value: str) -> bool:
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    r = requests.put(url, data=value, headers=headers)
    return r.text