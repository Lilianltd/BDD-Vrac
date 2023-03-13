from Stock import Stock

class Cart():
    def __init__(self) -> None:
        self.cart = []
    
    def addProduct(self , productName : str, quantity : float) -> None:
        self.cart.append([])
        self.cart[-1].append(productName)
        self.cart[-1].append(quantity)
        self.cart[-1].append(Stock.getProductPrice(productName)*quantity)

    def totalPriceCart(self) -> str:
        if self.cart == []:
            total = 0
        else:
            total = 0
            for buyItem in self.cart:
                #print(self.cart)
                total += buyItem[2]
            total = round(total*100)/100
        return total

    def getProductList(self) -> list:
        productList = []
        for product in self.cart:
            productList.append(product[0])
        return productList
    
    def productIndex(self,productName : str) -> int:
        k = -1
        for j, product in enumerate (self.getProductList()):
            if product == productName:
                return j
        return k
    
    def removeProduct(self,productName):
        k = self.productIndex(productName)
        if k != -1:
            del self.cart[k]
