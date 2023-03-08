import requests

def get(url : str) -> str:
    try :
        request = requests.get(url)
        return request.json()
    except requests.exceptions as err:
        print(err)

def post(url : str):
    try :
        request = requests.post(url)
    except requests.exceptions as err:
        print(err)

def put(url : str):
    requests.put(url)

def delet(url : str) -> None:
    requests.delete(url)


a = requests.post('https://lilianletard.ovh/BDD/API/Client/client.php?Nom=Deutsh&Prenom=Arthur')
print(a.text)