import sys
import json as js
from PySide2 import QtWidgets as qtw
from PySide2.QtCore import Qt, Slot, QAbstractTableModel
from PySide2 import QtGui as qtg

#Ui of Stock

class MainWinWidget(qtw.QWidget):
    """Widget central: C'est lui qui s'occupe de l'affichage des dossiers/fichiers"""
    def __init__(self, parent):
        super(MainWinWidget, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()
        layoutO = qtw.QHBoxLayout()
        self.output = OutputStock(self)
        layoutO.addWidget(self.output)
        layout.addLayout(layoutO)
        self.setLayout(layout)

class OutputStock(qtw.QGroupBox):
    def __init__(self, parent, font=None):
        super(OutputStock, self).__init__()
        if font is None: font = qtg.QFont('Times', 12)
        self.parent = parent
        layout = qtw.QVBoxLayout()
        self.output = qtw.QTableView()


        # self.output.selectionChanged.connect(self.update_format)
        with open('Data.json') as mon_fichier:
            self.data = js.load(mon_fichier)
    
        self.dataTable = self.dataExtract()
        self.model = TableStockModel(self.dataTable)
        self.output.setModel(self.model)
        layout.addWidget(self.output)
        self.setLayout(layout)
    
    def dataExtract(self):
        products = []
        for product in self.data:
            productName = product
            products.append([productName])
            if "Prix kg" in self.data[productName]:
                products[-1].append(self.data[productName]["Prix kg"])
                products[-1].append("")
            else:
                products[-1].append("")
                products[-1].append(self.data[productName]["Prix unite"])
            products[-1].append(self.data[productName]["quantite"])
        return products

class UpdateStock(qtw.QDialog):
    def __init__(self, parent) -> None:
        super(UpdateStock, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()

        self.productName = qtw.QLineEdit()
        self.productName.setPlaceholderText("Nom du produit")
        layout.addWidget(self.productName)

        self.quantityAdd = qtw.QLineEdit(self)
        self.quantityAdd.setPlaceholderText("Quantité à rajouté")
        layout.addWidget(self.quantityAdd)

        self.button = qtw.QPushButton("Validé", self)
        self.button.clicked.connect(self.setUpdate)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def setUpdate(self):
        with open('Data.json') as mon_fichier:
            data = js.load(mon_fichier)

        if self.productName.text() in data:
            data[self.productName.text()]["quantite"] += float(self.quantityAdd.text())

        with open('Data.json', 'w') as f:
            js.dump(data, f)
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
        with open('Data.json') as mon_fichier:
            data = js.load(mon_fichier)

        if self.productName not in data:
            data[self.productName.text()] = {}
            if self.priceSelect.currentText() == "Au kilo":
                data[self.productName.text()]["Prix kg"] = float(self.price.text())
            else:
                data[self.productName.text()]["Prix unite"] = float(self.price.text())

            data[self.productName.text()]["quantite"] = 0

        with open('Data.json', 'w') as f:
            js.dump(data, f)
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

class TableStockModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableStockModel, self).__init__()
        self.horizontalHeaders = [''] * 4
        self.setHeaderData(0, Qt.Horizontal, "Nom")
        self.setHeaderData(1, Qt.Horizontal, "Prix au kilo")
        self.setHeaderData(2, Qt.Horizontal, "Prix à l'unité")
        self.setHeaderData(3, Qt.Horizontal, "Quantité")
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

#Ui of Vente

class MainVenteWidget(qtw.QWidget):
    def __init__(self):
        super(MainVenteWidget, self).__init__()
        layout = qtw.QVBoxLayout()
        layoutO = qtw.QHBoxLayout()
        self.output = OutputVente()
        layoutO.addWidget(self.output)
        layout.addLayout(layoutO)
        self.setLayout(layout)

class NewClient(qtw.QWidget):
    def __init__(self,parent) -> None:
        super(NewClient, self).__init__()
        self.parent = parent

        with open('Data.json') as mon_fichier:
            self.data = js.load(mon_fichier)
        products = []
        for ele in self.data:
            products.append(ele)
        mon_fichier.close()

        self.totalCart()
        self.setMinimumSize(500,500)

        self.myLayout = qtw.QVBoxLayout()
        myLayout1 = qtw.QHBoxLayout()
        mylayout2 = qtw.QHBoxLayout()
        mylayout3 = qtw.QHBoxLayout()
        self.productSell = qtw.QTableView()
        self.model = TableCartModel(self.parent.cart)
        self.productSell.setModel(self.model)

        self.productSelect = qtw.QComboBox(self)
        self.productSelect.setPlaceholderText("Produits")
        self.productSelect.addItems(products)

        self.familyName = qtw.QLineEdit()
        self.familyName.setPlaceholderText("Nom")

        self.name = qtw.QLineEdit()
        self.name.setPlaceholderText("Prenom")

        self.labelPrice = qtw.QLabel()
        self.labelPrice.setText(self.total)

        self.comboBoxPayWay = qtw.QComboBox()
        self.comboBoxPayWay.addItems({"Lydia","Espece"})

        self.quantity = qtw.QLineEdit(self)
        self.quantity.setPlaceholderText("Quantité")

        self.button = qtw.QPushButton("Ajouter au panier", self)
        self.button.clicked.connect(self.newItems)

        self.buttonValidate = qtw.QPushButton("Validé le panier",self)
        self.buttonValidate.clicked.connect(self.validateCart)

        self.myLayout.addWidget(self.productSell)
        myLayout1.addWidget(self.productSelect)
        myLayout1.addWidget(self.quantity)
        myLayout1.addWidget(self.button)
        
        mylayout2.addWidget(self.familyName)
        mylayout2.addWidget(self.name)

        mylayout3.addWidget(self.labelPrice)
        mylayout3.addWidget(self.comboBoxPayWay)
        
        self.myLayout.addLayout(mylayout3)
        self.myLayout.addLayout(mylayout2)
        self.myLayout.addLayout(myLayout1)
        self.myLayout.addWidget(self.buttonValidate)
        self.setLayout(self.myLayout)
        
    def newItems(self):
        currentProduct = self.productSelect.currentText()

        with open('Data.json') as Stock:
            self.stock = js.load(Stock)

        if str.isdecimal(self.quantity.text()) and self.stock[currentProduct]["quantite"] > float(self.quantity.text()) :
            self.parent.cart.append([])
            self.parent.cart[-1].append(currentProduct)
            if "Prix kg" in self.data[currentProduct]:
                self.parent.cart[-1].append(float(self.quantity.text()))
                self.parent.cart[-1].append(self.data[currentProduct]["Prix kg"]*float(self.quantity.text()))
            else:
                self.parent.cart[-1].append(float(self.quantity.text()))
                self.parent.cart[-1].append(self.data[currentProduct]["Prix unite"]*float(self.quantity.text()))
            self.totalCart()
            self.labelPrice.setText(self.total)
            layout_Table = self.myLayout.itemAt(0)
            layout_Table.widget().deleteLater()
            self.productSell = qtw.QTableView()
            self.model = TableCartModel(self.parent.cart)
            self.productSell.setModel(self.model)
            self.myLayout.insertWidget(0,self.productSell,0)
            self.setLayout(self.myLayout)
            self.quantity.setText("")
        else:
            self.quantity.setText("")
            if str.isdecimal(self.quantity.text()) == False: 
                widerror = ErrorMessage("Format invalid")
                widerror.exec_()
            else:
                widerror = ErrorMessage("Stock insuffisant")
                widerror.exec_()

    def validateCart(self):
        self.parent.cart.append(self.familyName.text())
        self.parent.cart.append(self.name.text())
        self.parent.cart.append(self.comboBoxPayWay.currentText())
        self.close()

    def totalCart(self):
        if self.parent.cart == []:
            self.total = "Total :"
        else:
            total = 0
            for buyItem in self.parent.cart:
                total += buyItem[2]
            self.total = "Total : " + str(total)

class TableCartModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableCartModel, self).__init__()
        self.horizontalHeaders = [''] * 3
        self.setHeaderData(0, Qt.Horizontal, "Produit")
        self.setHeaderData(1, Qt.Horizontal, "Quantité")
        self.setHeaderData(2, Qt.Horizontal, "Prix")
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

class TableVenteModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableVenteModel, self).__init__()
        self.horizontalHeaders = [''] * 3
        self.setHeaderData(0, Qt.Horizontal, "Produit")
        self.setHeaderData(1, Qt.Horizontal, "Quantité")
        self.setHeaderData(2, Qt.Horizontal, "Nombre clients")
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

class OutputVente(qtw.QGroupBox):
    def __init__(self, font=None):
        super(OutputVente, self).__init__()
        if font is None: font = qtg.QFont('Times', 12)
        self.mylayout = qtw.QVBoxLayout()
        self.output = qtw.QTableView()
        with open('Vente semaine.json') as mon_fichier:
            self.data = js.load(mon_fichier)
        

        self.dataTable = self.dataExtract()
        self.model = TableVenteModel(self.dataTable)
        self.output.setModel(self.model)
        self.mylayout.addWidget(self.output)

        self.buttonNewClient = qtw.QPushButton()
        self.buttonNewClient.setText("Nouveau Client")
        self.buttonNewClient.clicked.connect(self.newClient)
        self.mylayout.addWidget(self.buttonNewClient)

        self.setLayout(self.mylayout)
    
    def newClient(self):
        self.windows = []

        self.windows.append([])
        self.windows[-1].append([])
        self.windows[-1].append(NewClient(self))

        self.windows[-1][1].show()
        with open("Data.json") as Stocks:
            stock = js.load(Stocks)
        Stocks.close()

        with open("Vente semaine.json") as curentSell:
            data = js.load(curentSell)

        data[len(data)] = {}
        for k in range (len(self.cart)-3):
            data[len(data)-1][k] = self.cart[k]
            stock[self.cart[k][0]]["quantite"] -= self.cart[k][1]

        data[len(data)-1]["Nom"] = self.cart[-3]
        data[len(data)-1]["Prenom"] = self.cart[-2]
        data[len(data)-1]["Mode paiemant"] = self.cart[-1]
        curentSell.close()

        with open("Vente semaine.json",'w') as curentSell:
            data = js.dump(data,curentSell)
        curentSell.close()

        with open("Data.json",'w') as Stocks:
            stock = js.dump(stock, Stocks)
        Stocks.close()

        self.dataTable = self.dataExtract()
        layout_Table = self.mylayout.itemAt(0)
        layout_Table.widget().deleteLater()
        self.output = qtw.QTableView()
        self.model = TableVenteModel(self.dataTable)
        self.output.setModel(self.model)
        self.mylayout.insertWidget(0,self.output,0)
        self.setLayout(self.mylayout)


    def dataExtract(self):
        products = []
        with open("Vente semaine.json") as curentSell:
            data = js.load(curentSell)

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

#

class MainWinMar(qtw.QMainWindow):
    def __init__(self):
        super(MainWinMar, self).__init__()

        # Paramétrage général

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
        stock_action[1].triggered.connect(lambda: self.delProduct)
        stock_action[2] = qtw.QAction("Réapprovisionner", self)
        stock_action[2].triggered.connect(self.updateStock)
        stock_action[3] = qtw.QAction("Modifier un produit", self)
        stock_action[3].triggered.connect(lambda: self.modifyProduct)

        for i in range(len(stock_action)):
            self.menu[0].addAction(stock_action[i])

        # Création des sous-menus pour les clients

        client_action = [None, None]
        client_action[0] = qtw.QAction("Nouveau Client", self)
        client_action[0].triggered.connect(lambda: self.connexion)
        client_action[0].setShortcut("Ctrl+O")
        client_action[1] = qtw.QAction("Supprimer Client", self)
        client_action[1].triggered.connect(self.connexion)

        for i in client_action:
            self.menu[1].addAction(i)

        connexion_action = qtw.QAction("Connexion base de données", self)
        connexion_action.triggered.connect(self.connexion)

        self.menu[2].addAction(connexion_action)

        vente_action = [None,None,None]
        vente_action[0] = qtw.QAction("Accéder à une semaine précédente", self)
        vente_action[0].triggered.connect(lambda: self.connexion)
        vente_action[1] = qtw.QAction("Nouvelle semaine", self)
        vente_action[1].triggered.connect(self.createNewDay)
        vente_action[2] = qtw.QAction("Reprendre une semaine", self)
        vente_action[2].triggered.connect(self.connexion)

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

    def delProduct():
        print("test2")

    def modifyProduct():
        print("test3")

    def createNewDay(self):
        if self.connected == True:
            self.widget = MainVenteWidget()
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

class ErrorMessage(qtw.QDialog):
    def __init__(self,message):
        super(ErrorMessage, self).__init__()
        self.setWindowTitle("Erreur")
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QLabel()
        self.productName.setText(message)
        layout.addWidget(self.productName)
        self.setLayout(layout)

if __name__ == '__main__':
    # Create the Qt Application
    app = qtw.QApplication(sys.argv)
    # Create and show the form
    form = MainWinMar()
    form.show()
    # Run the main Qt loop
    app.exec_()
