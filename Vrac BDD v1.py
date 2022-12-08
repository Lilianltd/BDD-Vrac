import sys
import json as js
from PySide2 import QtWidgets as qtw
from PySide2.QtCore import Qt, Slot, QAbstractTableModel
from PySide2 import QtGui as qtg
import csv
import time
from os import listdir
#Ui of Stock

class MainWinWidget(qtw.QWidget):
    """Widget central: C'est lui qui s'occupe de l'affichage des dossiers/fichiers"""
    def __init__(self, parent):
        super(MainWinWidget, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()
        layoutO = qtw.QHBoxLayout()
        self.output = OutputStock()
        layoutO.addWidget(self.output)
        layout.addLayout(layoutO)
        self.setLayout(layout)

class OutputStock(qtw.QGroupBox):
    def __init__(self):
        super(OutputStock, self).__init__()
        layout = qtw.QVBoxLayout()
        self.output = qtw.QTableView()
        self.dataTable = Stock.tableExtract()
        self.model = TableModel(self.dataTable,["Nom","Prix au kilo","Prix à l'unité","Quantité"])
        self.output.setModel(self.model)
        layout.addWidget(self.output)
        self.setLayout(layout)

class UpdateStock(qtw.QDialog):
    def __init__(self, parent) -> None:
        super(UpdateStock, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QComboBox()
        self.productName.addItems(Stock.getProductList())
        layout.addWidget(self.productName)
        self.quantityAdd = qtw.QLineEdit(self)
        self.quantityAdd.setPlaceholderText("Quantité à rajouté")
        layout.addWidget(self.quantityAdd)
        self.button = qtw.QPushButton("Validé", self)
        self.button.clicked.connect(self.setUpdate)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def setUpdate(self):
        Stock.replenish(self.productName.currentText(),float(self.quantityAdd.text()))
        self.close()

class AddProduct(qtw.QDialog):
    def __init__(self, parent) -> None:
        super(AddProduct, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QLineEdit()
        self.productName.setPlaceholderText("Nom du produit")
        layout.addWidget(self.productName)
        self.price = qtw.QLineEdit(self)
        self.price.setPlaceholderText("Prix")
        layout.addWidget(self.price)

        self.priceSelect = qtw.QComboBox(self)
        self.priceSelect.setPlaceholderText("Type de prix")
        self.priceSelect.addItems({"Au kilo", "A l'unité"})
        layout.addWidget(self.priceSelect)

        self.button = qtw.QPushButton("Ajouter", self)
        self.button.clicked.connect(self.setAdd)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setAdd(self):
        product = [self.productName.text(),self.priceSelect.currentText(),self.price.text()]
        Stock.addProduct(product)
        self.close()
        
class ConnexionWidget(qtw.QDialog):
    def __init__(self, parent, box=False) -> None:
        super(ConnexionWidget, self).__init__()
        self.parent = parent
        self.isBox = box
        layout = qtw.QVBoxLayout()
        self.id = qtw.QLineEdit()
        self.id.setPlaceholderText("Identifiant")
        self.id.setObjectName("id")
        layout.addWidget(self.id)
        self.mdp = qtw.QLineEdit(self)
        self.mdp.setEchoMode(qtw.QLineEdit.PasswordEchoOnEdit)
        self.mdp.setObjectName("mdp")
        self.mdp.setPlaceholderText("Mot de passe")
        layout.addWidget(self.mdp)
        self.button = qtw.QPushButton("Connexion", self)
        self.button.clicked.connect(self.setConnexion)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setConnexion(self):
        identifiant_list = {}
        identifiant_list["lilian"] = "lilian"
        if self.id.text() in identifiant_list and identifiant_list[self.id.text()] == self.mdp.text():
            form.connected = True
            self.close()
            
        else:
            self.mdp.setText("")
            self.id.setText("")

class DelProduct(qtw.QDialog):
    def __init__(self) -> None:
        super(DelProduct, self).__init__()
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QComboBox()
        self.productName.addItems(Stock.getProductList())
        self.productName.setPlaceholderText("Nom du produit")
        layout.addWidget(self.productName)
        self.button = qtw.QPushButton("Supprimer", self)
        self.button.clicked.connect(self.setDel)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setDel(self):
        Stock.delProduct(self.productName.currentText())
        self.close()

#Ui of Vente

class MainVenteWidget(qtw.QWidget):
    def __init__(self,date):
        super(MainVenteWidget, self).__init__()
        layout = qtw.QVBoxLayout()
        layoutO = qtw.QHBoxLayout()
        self.output = OutputVente(date)
        layoutO.addWidget(self.output)
        layout.addLayout(layoutO)
        self.setLayout(layout)

class NewClient(qtw.QWidget):
    def __init__(self,parent) -> None:
        super(NewClient, self).__init__()
        self.parent = parent
        self.cart : Cart = Cart()
        self.layouts = []
        self.products = Stock.getProductList()
        self.setMinimumSize(500,500) 
        
        self.myLayout = qtw.QVBoxLayout()
        self.layouts.append(self.myLayout)
        
        for k in range(0,3):
            self.layouts.append(qtw.QHBoxLayout())

        self.productSell = qtw.QTableView()
        self.model = TableModel(self.cart.cart,["Produits","Quantité","Prix"])
        self.productSell.setModel(self.model)

        self.productSelect = qtw.QComboBox(self)
        self.productSelect.setPlaceholderText("Produits")
        self.productSelect.addItems(self.products)

        self.familyName = qtw.QLineEdit()
        self.familyName.setPlaceholderText("Nom")

        self.name = qtw.QLineEdit()
        self.name.setPlaceholderText("Prenom")

        self.labelPrice = qtw.QLabel()
        self.labelPrice.setText(Cart.totalPriceCart(self.cart))

        self.comboBoxPayWay = qtw.QComboBox()
        self.comboBoxPayWay.addItems({"Lydia","Espece"})

        self.quantity = qtw.QLineEdit(self)
        self.quantity.setPlaceholderText("Quantité")

        self.button = qtw.QPushButton("Ajouter au panier", self)
        self.button.clicked.connect(self.newItems)

        self.buttonValidate = qtw.QPushButton("Validé le panier",self)
        self.buttonValidate.clicked.connect(self.validateCart)

        self.myLayout.addWidget(self.productSell)
        self.layouts[1].addWidget(self.productSelect)
        self.layouts[1].addWidget(self.quantity)
        self.layouts[1].addWidget(self.button)
        self.layouts[2].addWidget(self.familyName)
        self.layouts[2].addWidget(self.name)
        self.layouts[3].addWidget(self.labelPrice)
        self.layouts[3].addWidget(self.comboBoxPayWay)
        
        for k in range(0,3):
            self.myLayout.addLayout(self.layouts[3-k])
            
        self.myLayout.addWidget(self.buttonValidate)
        self.setLayout(self.myLayout)
        
    def newItems(self):
        if isfloat(self.quantity.text()):
            if Stock.isProductAvailable(self.productSelect.currentText(),float(self.quantity.text())):
                Cart.addProduct(self.cart, self.productSelect.currentText(), float(self.quantity.text()))
                self.labelPrice.setText(Cart.totalPriceCart(self.cart))
                layout_Table = self.myLayout.itemAt(0)
                layout_Table.widget().deleteLater()
                self.productSell = qtw.QTableView()
                self.model = TableModel(self.cart.cart,["Produits","Quantité","Prix"])
                self.productSell.setModel(self.model)
                self.myLayout.insertWidget(0,self.productSell,0)
                self.setLayout(self.myLayout)
                self.quantity.setText("")
            else:
                widerror = ErrorMessage("Stock insuffisant")
                widerror.exec_()
        else:
            self.quantity.setText("")
            widerror = ErrorMessage("Format invalid")
            widerror.exec_()
            
    def validateCart(self):
        if self.name.text() != '' and self.familyName.text() != '':
            DaySell.addCart(self.cart, self.familyName.text(),self.name.text(),self.comboBoxPayWay.currentText(),self.parent.date)
            self.parent.tableActualisation()
            self.close()
        else:
            widerror = ErrorMessage("Enter a Family name and a name")
            widerror.exec_()
    
class OutputVente(qtw.QGroupBox):
    def __init__(self, date,font=None):
        super(OutputVente, self).__init__()
        self.windows = []
        self.date = date
        if font is None: font = qtg.QFont('Times', 12)
        self.mylayout = qtw.QVBoxLayout()
        self.output = qtw.QTableView()

    
        self.model = TableModel(DaySell.tableExtract(self.date),["Produits","Quantité","Nombre clients"])
        self.output.setModel(self.model)
        self.mylayout.addWidget(self.output)
        self.buttonNewClient = qtw.QPushButton()
        self.buttonNewClient.setText("Nouveau Client")
        self.buttonNewClient.clicked.connect(self.newClient)
        self.mylayout.addWidget(self.buttonNewClient)
        self.setLayout(self.mylayout)
        self.buttonCloseVrac = qtw.QPushButton()
        self.buttonCloseVrac.setText("Quitter")
        self.buttonCloseVrac.clicked.connect(self.closeSell)

    def closeSell(self):
        self.close()

    def newClient(self):
        self.windows.append([])
        self.windows[-1].append([])
        self.windows[-1].append(NewClient(self))
        self.windows[-1][1].show()

    def tableActualisation(self):
        layout_Table = self.mylayout.itemAt(0)
        layout_Table.widget().deleteLater()
        self.output = qtw.QTableView()
        self.model = TableModel(DaySell.tableExtract(self.date),["Produits","Quantité","Nombre clients"])
        self.output.setModel(self.model)
        self.mylayout.insertWidget(0,self.output,0)
        self.setLayout(self.mylayout)

# 

class MainWinMar(qtw.QMainWindow):

    def __init__(self):
        super(MainWinMar, self).__init__()
        # Création des widgets
        self.connected = False

        # Création de la fenêtre et de son pourtour
        self.window().setWindowTitle("BDD Vrac")  
        self.setMinimumSize(700, 700)
        self.resize(1300, 900)
        self.mainMenu = self.menuBar()
        self.mainStatBar = self.statusBar()

        self.menu = [None for i in range(4)]
        self.menu[0] = self.mainMenu.addMenu("&Stock")
        self.menu[1] = self.mainMenu.addMenu("&Client")
        self.menu[2] = self.mainMenu.addMenu("&Connexion")
        self.menu[3] = self.mainMenu.addMenu("&Vente")

        # Création des sous-menus pour les stocks
        stock_action = [None for i in range(4)]
        stock_action[0] = qtw.QAction("Rajouter un produit", self)
        stock_action[0].triggered.connect(self.addProduct)
        stock_action[1] = qtw.QAction("Supprimer un produit", self)
        stock_action[1].triggered.connect(self.delProduct)
        stock_action[2] = qtw.QAction("Réapprovisionner", self)
        stock_action[2].triggered.connect(self.updateStock)
        stock_action[3] = qtw.QAction("Modifier un produit", self)
        stock_action[3].triggered.connect(self.modifyProduct)

        for i in range(len(stock_action)):
            self.menu[0].addAction(stock_action[i])

        # Création des sous-menus pour les clients

        client_action = [None, None]
        client_action[0] = qtw.QAction("Nouveau Client", self)
        client_action[0].triggered.connect(lambda: self.connexion)
        client_action[0].setShortcut("Ctrl+O")
        client_action[1] = qtw.QAction("Supprimer Client", self)
        client_action[1].triggered.connect(lambda: self.connexion)

        for i in client_action:
            self.menu[1].addAction(i)

        connexion_action = qtw.QAction("Connexion base de données", self)
        connexion_action.triggered.connect(self.connexion)

        self.menu[2].addAction(connexion_action)

        vente_action = [None,None,None]
        vente_action[0] = qtw.QAction("Accéder à un jour", self)
        vente_action[0].triggered.connect(self.accessPreviousDay)
        vente_action[1] = qtw.QAction("Vente jour actuel", self)
        vente_action[1].triggered.connect(self.createNewDay)
        vente_action[2] = qtw.QAction("Extraire au format csv", self)
        vente_action[2].triggered.connect(self.extracttocsv)

        for act in vente_action:
            self.menu[3].addAction(act)
    @Slot()
    def connexion(self):
        wid = ConnexionWidget(self, )
        wid.exec()
        if self.connected == True:
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)

    def updateStock(self):
        if self.connected == True:
            wid = UpdateStock(self)
            wid.exec()
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def addProduct(self):
        if self.connected == True:
            wid = AddProduct(self)
            wid.exec()
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def delProduct(self):
        if self.connected == True:
            wid = DelProduct()
            wid.exec()
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def modifyProduct(self):
        if self.connected == True:
            wid = ModifyProduct()
            wid.exec_()
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def createNewDay(self):
        self.time = time.gmtime()
        fileName = str(self.time.tm_mday) + '_' + str(self.time.tm_mon) + '_' + str(self.time.tm_year)

        try: 
            with open(fileName + ".json"): 
                pass
        
        except IOError:
            DaySell.write({},fileName)

        if self.connected == True:
            self.widget = MainVenteWidget(fileName)
            self.widget.date = fileName
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def accessPreviousDay(self):
        self.date = ''
        wid = DialogChooseSell(self)
        wid.exec_()
        if self.connected == True:
            self.widget = MainVenteWidget(self.date)
            self.widget.date = self.date
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()
        
    def extracttocsv(self):
        self.date = ''
        wid = DialogChooseSell(self)
        wid.exec_()
        DaySell.csvExtract(self.date)

class ErrorMessage(qtw.QDialog):
    def __init__(self,message):
        super(ErrorMessage, self).__init__()
        self.setWindowTitle("Erreur")
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QLabel()
        self.productName.setText(message)
        layout.addWidget(self.productName)
        self.setLayout(layout)

class TableModel(QAbstractTableModel):
    def __init__(self, data,headerName):        # Paramétrage général        # Paramétrage général

        super(TableModel, self).__init__()
        self.horizontalHeaders = [''] * len(headerName)
        for k in range(0,len(headerName)):
            self.setHeaderData(k, Qt.Horizontal, headerName[k])
        self._data = data

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontalHeaders[section]
            except:
                pass
        return super().headerData(section, orientation, role)
    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class Stock():
    def read() -> dict:
        with open("Data.json") as stock:
            data = js.load(stock)
            stock.close()
            return data

    def write(data) -> None:
        with open("Data.json","w") as stock:
            js.dump(data,stock)

    def getProductList() -> list: 
        data = Stock.read()
        products = []
        for ele in data:
            products.append(ele)
        return products
    
    def addProduct(product : list) -> None:
        stock = Stock.read()

        if product[0] not in stock: #product[0] is the name of the given product
            stock[product[0]] = {} 
            if product[1] == "Au kilo": #product[1] is the selected price type
                stock[product[0]]["Prix kg"] = float(product[2]) #product[2] is the price
            else:
                stock[product[0]]["Prix unite"] = float(product[2])

            stock[product[0]]["quantite"] = 0

        Stock.write(stock)

    def replenish(productName : str, quantity : float) -> None:
        stock = Stock.read()
        if productName in stock:
            stock[productName]["quantite"] += quantity
        Stock.write(stock)
    
    def tableExtract() -> list:
        stock = Stock.read()
        products = []
        for product in stock:
            productName = product
            products.append([productName])
            if "Prix kg" in stock[productName]:
                products[-1].append(stock[productName]["Prix kg"])
                products[-1].append("")
            else:
                products[-1].append("")
                products[-1].append(stock[productName]["Prix unite"])
            products[-1].append(stock[productName]["quantite"])
        return products
    
    def isProductAvailable(productName : str, quantitySell : float) -> bool:
        stock = Stock.read()
        if stock[productName]["quantite"] >= quantitySell:
            return True
        return False 

    def getProductPrice(productName : str) -> float:
        stock = Stock.read()
        if "Prix kg" in stock[productName]:
            return stock[productName]['Prix kg']
        return stock[productName]['Prix unite']

    def delProduct(productName : str) -> None:
        stock = Stock.read()
        del stock[productName]
        Stock.write(stock)  

    def modifyProduct(productName : str, newPrice : float) -> None:
        stock = Stock.read()
        if "Prix kg" in stock[productName]:
            stock[productName]["Prix kg"] = newPrice
        else:
            stock[productName]['Prix unite'] = newPrice
        Stock.write(stock)


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

class DaySell():
    def read(fileName : str) -> None:
        with open(fileName + ".json") as curentSell:
            data = js.load(curentSell)
        return data
    
    def write(data : dict, fileName : str) -> None:
        with open(fileName + ".json","w") as curentSell:
            js.dump(data,curentSell)

    def tableExtract(fileName : str) -> list:
        products = []
        data = DaySell.read(fileName)
        productName = []
        for commande in data:
            thisCommande = data[commande]
            for k in range(0,len(thisCommande)-3):
                productSell = thisCommande[str(k)]
                if productSell[0] not in productName:
                    products.append([productSell[0],productSell[1],1])
                    productName.append(productSell[0])
                else:
                    editProduct = products[productName.index(productSell[0])]
                    editProduct[2] += 1
                    editProduct[1] += productSell[1]
                    products[productName.index(productSell[0])] = editProduct
        return products

    def addCart(cart : Cart, familyName : str, name : str, payWay : str, fileName : str):
        data = DaySell.read(fileName)
        data[len(data)] = {}
        for k in range (len(cart.cart)):
            data[len(data)-1][k] = cart.cart[k]
            Stock.replenish(cart.cart[k][0], -cart.cart[k][1])
        data[len(data)-1]["Nom"] = familyName
        data[len(data)-1]["Prenom"] = name
        data[len(data)-1]["Mode paiement"] = payWay
        DaySell.write(data,fileName)
    
    def csvExtract(date : str):
        data = DaySell.read(date)
        with open(date + ".csv","w") as fcsv:
            writer = csv.writer(fcsv, delimiter=';',lineterminator='\n')  
            table = []  
            lydia = 0
            espece = 0
            for element in data:
                client = data[element]                
                head = ["client n°"+str(int(element)+1),client["Nom"],client["Prenom"],client["Mode paiement"],0]
                table.append(head)
                j = 0
                while str(j) in client:
                    table.append(client[str(j)])
                    table[-2-j][4] += float(client[str(j)][2])
                    j+=1
                if client["Mode paiement"] == "Espece":
                    espece += table[-1-j][4]
                else:
                    lydia += table[-1-j][4]
                table.append([""])
            
            for k in range(0,2):
                table[0].append('')
            table[0].append('Total Lydia :')
            table[0].append(round(lydia*100)/100)
            
            for k in range(0,4):
                table[1].append('')
            table[1].append('Total Espece :')
            table[1].append(round(espece*100)/100)
            writer.writerows(table)
    
    def getDate():
        dateVrac = []
        for element in listdir():
            result = 1
            if '.json' not in element or len(element) != 14:
                result *= 0
            if len(element) == 14:
                if element[1] != '_' or element[4] != '_':
                    result *= 0
                for k in {0,2,3,5,6,7,8}:
                    if str.isdigit(element[k]) == False:
                        result *= 0
            if result == 1:
                dateVrac.append(element[0:9])
        return dateVrac

class DialogChooseSell(qtw.QDialog):
    def __init__(self,parent) -> None:
        super(DialogChooseSell, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()
        self.vracDate = qtw.QLabel()
        self.vracDate.setText("Date du vrac")
        layout.addWidget(self.vracDate)

        self.disponibleVracDate = qtw.QComboBox(self)
        self.disponibleVracDate.addItems(DaySell.getDate())
        layout.addWidget(self.disponibleVracDate)

        self.button = qtw.QPushButton("Valider", self)
        self.button.clicked.connect(self.validate)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def validate(self):
        self.parent.date = self.disponibleVracDate.currentText() 
        self.close()

class ModifyProduct(qtw.QDialog):
    def __init__(self) -> None:
        super(ModifyProduct, self).__init__()
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QComboBox()
        self.productName.addItems(Stock.getProductList())
        layout.addWidget(self.productName)
        
        self.price = qtw.QLineEdit(self)
        self.price.setPlaceholderText("Prix")
        layout.addWidget(self.price)

        self.button = qtw.QPushButton("Modifier", self)
        self.button.clicked.connect(self.setModify)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setModify(self):
        Stock.modifyProduct(self.productName.currentText(),float(self.price.text()))
        self.close()

def isfloat(value) -> bool:
  try:
    float(value)
    return True
  except ValueError:
    return False

if __name__ == '__main__':
    # Create the Qt Application
    app = qtw.QApplication(sys.argv)
    # Create and show the form
    form = MainWinMar()
    form.show()
    # Run the main Qt loop
    app.exec_()

