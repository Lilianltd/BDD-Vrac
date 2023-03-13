import Requête as req

class Client():
    def addClient(familyName : str, name:str) -> None:
        url = "https://lilianletard.ovh/BDD/API/Client/client.php?Nom=" + familyName +"&Prenom=" + name
        print(url)
        req.post(url)

    def delClient(familyName : str, name:str) -> None:
        url = "https://lilianletard.ovh/BDD/API/Client/client.php?Nom=" + familyName +"&Prenom=" + name
        req.delet(url)

    def findNom(prenom:str) -> list: #find the prenom having a given Nom
        if prenom == None:
            print("dezd")
        else:
            print("llea")

    def getClient(Nom : str, Prenom : str) -> int:
        url = "https://lilianletard.ovh/BDD/API/Client/client.php?Nom="+Nom+"&Prenom="+Prenom
        response = req.get(url)
        if response ==  []:
            return None 
        return response[0]

    def findPrenom(nom:str) ->list: #find the prenom having a given Nom
        if nom == None:
            print("dezd")
        else:
            print("llea")

    def clientList(text : str) -> list:
        clientList = []
        url = "https://lilianletard.ovh/BDD/API/Client/client.php"
        response = req.get(url)
        for client in response:
            clientList.append(client[0] + " " + client[1])
        return clientList