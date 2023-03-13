import requests

def get(url : str) -> str:
    request = requests.get(url)
    return request.json()

def post(url : str):
    request = requests.post(url)


def put(url : str):
    requests.put(url)

def delet(url : str) -> None:
    requests.delete(url)


