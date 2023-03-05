import Requête as req



class Stock():

    def productExist(Name : str) -> list:
        url = "https://lilianletard.ovh/BDD/API/Stock/product.php?Nom=" + Name
        result = list(req.get(url))
        if len(result) == 0:
            return None
        return result[0]

    def getProductList() -> list: 
        return list(req.get("https://lilianletard.ovh/BDD/API/Stock/product.php?getName=True"))
    
    def addProduct(product : list) -> None:
        if Stock.productExist(product[0]) == None:
            url = "https://lilianletard.ovh/BDD/API/Stock/product.php?Nom=" + product[0] + "&Prix=" + product[2] + "&Type="
            if product[1] == "Au kilo": #product[1] is the selected price type
                url += "0"
            else:
                url += "1"
            req.post(url)


    def replenish(productName : str, quantity : float) -> None:
        url = "https://lilianletard.ovh/BDD/API/Stock/quantity.php?Nom="+ productName + '&Quantite='
        if Stock.productExist(productName) != None:
            url += str(Stock.getProductQuantity(productName) + quantity)
        req.put(url)

    def tableExtract() -> list:
        products = []
        for productName in Stock.getProductList():
            product = Stock.productExist(productName)
            products.append([product[0],str(product[1]),product[3]])
            if product[2] == '0': #product[1] is the selected price type
                products[-1][1] += " / kg"
            else:
                products[-1][1] += " / unité"
        return products
    
    def getProductQuantity(productName : str) -> float:
        return float(req.get("https://lilianletard.ovh/BDD/API/Stock/quantity.php?Nom="+productName)[0])

    def isProductAvailable(productName : str, quantitySell : float) -> bool:
        if Stock.getProductQuantity(productName) >= quantitySell:
            return True
        return False 

    def getProductPrice(productName : str) -> float:
        return float(req.get("https://lilianletard.ovh/BDD/API/Stock/price.php?Nom="+productName)[0])

    def delProduct(productName : str) -> None:
        req.delet("https://lilianletard.ovh/BDD/API/Stock/product.php?Nom="+productName)

    def modifyProduct(productName : str, newPrice : float) -> None:
        url = "https://lilianletard.ovh/BDD/API/Stock/price.php?Nom="+ productName + '&Prix='
        if Stock.productExist(productName) != None:
            url += str(newPrice)
        req.put(url)