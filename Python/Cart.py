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
            totalstr = "Total :"
        else:
            total = 0
            for buyItem in self.cart:
                #print(self.cart)
                total += buyItem[2]
            totalstr = "Total : " + str(total)
        return totalstr