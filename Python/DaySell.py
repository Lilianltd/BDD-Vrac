import csv
from Client import Client
from Stock import Stock
from Cart import Cart
import Requête as req

class DaySell():
    
    def tableExtract(date : str) -> list:
        sell = list(req.get("https://lilianletard.ovh/BDD/API/Factures/facture.php?tableExtract=product&date=" + date))
        products = []
        productName = []
        for commande in sell: # commande is like that : [["product1","product2"][q1,q2]]
            for k in range (0,len(commande[0])):
                productSell = commande[0][k]
                if productSell not in productName:
                    products.append([productSell,float(commande[1][k]),1])
                    productName.append(productSell)
                else:
                    editProduct = products[productName.index(productSell)]
                    editProduct[2] += 1
                    editProduct[1] += float(commande[1][k])
                    products[productName.index(productSell)] = editProduct
        return products
    
    def clientExtract(date : str) -> list:
        sell = list(req.get("https://lilianletard.ovh/BDD/API/Factures/facture.php?tableExtract=client&date=" + date))
        lydia = 0
        espece = 0
        for s in sell:
            if s[3] == "Espece":
                espece += float(s[2])
            else:
                lydia += float(s[2])
        return sell,espece,lydia



    def addCart(cart : Cart, familyName : str, name : str, payWay : str, fileName : str):
        idClient = Client.getClient(familyName,name)
        idAchat = req.get("https://lilianletard.ovh/BDD/API/Achat/achat.php?lastId=True") + 1
        urlFacture = "https://lilianletard.ovh/BDD/API/Factures/facture.php?idAchat=" + str(idAchat) + "&idClient=" + str(idClient) + "&total=" + str(cart.totalPriceCart()) + "&payWay=" + payWay

        product = ""
        quantite = ""
        prix = ""
        for k in range (len(cart.cart)): #create productlist as product1&&product2 ... idem from quantity and price
            if k == len(cart.cart)-1:
                product += str(cart.cart[k][0])
                quantite += str(cart.cart[k][1])
                prix += str(cart.cart[k][2])
            else:
                product += str(cart.cart[k][0])+"||"
                quantite += str(cart.cart[k][1])+"||"
                prix += str(cart.cart[k][2])+"||"

            Stock.replenish(cart.cart[k][0], -cart.cart[k][1])
        
        urlAchat = "https://lilianletard.ovh/BDD/API/Achat/achat.php?Liste="+product+"&Quantite="+quantite+"&Prix="+prix
        req.post(urlAchat)
        req.post(urlFacture)

    
    def csvExtract(date : str):
        data = list(req.get("https://lilianletard.ovh/BDD/API/Factures/facture.php?csv=True&date="+date))
        with open(date + ".csv","w") as fcsv:
            writer = csv.writer(fcsv, delimiter=';',lineterminator='\n')  
            table = []  
            lydia = 0
            espece = 0
            for element in data:                
                head = [element[0],element[1],element[2],element[3]]
                table.append(head)
                for k in range (0,len(element[4])):
                    product = [element[4][k],element[5][k],element[6][k]]
                    table.append(product)
                if element[2] == "Espece":
                    espece += float(element[3])
                else:
                    lydia += float(element[3])
                table.append([""])
            
            for k in range(0,2):
                table[0].append('')
            table[0].append('Total Lydia :')
            table[0].append(round(lydia*100)/100)
            
            for k in range(0,3):
                table[1].append('')
            table[1].append('Total Espece :')
            table[1].append(round(espece*100)/100)
            writer.writerows(table)
    
    def getDate():
        dateVrac = req.get("https://lilianletard.ovh/BDD/API/Factures/facture.php")
        return dateVrac

