import sys
from PySide2 import QtWidgets as qtw
from PySide2.QtCore import Qt, Slot, QAbstractTableModel
from PySide2 import QtGui as qtg
import time
from Client import Client
from Stock import Stock
from Cart import Cart
from DaySell import DaySell
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
        self.model = TableModel(self.dataTable,["Nom","Prix","Quantité"])
        layout.addWidget(self.model)
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
        self.quantityAdd.setPlaceholderText("Quantité à rajouter")
        layout.addWidget(self.quantityAdd)
        self.button = qtw.QPushButton("Valider", self)
        self.button.clicked.connect(self.setUpdate)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def setUpdate(self):
        Stock.replenish(self.productName.currentText(),float(self.quantityAdd.text()))
        self.close()

class AddClient(qtw.QDialog):
    def __init__(self, parent) -> None:
        super(AddClient, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()
        self.familyName = qtw.QLineEdit()
        self.familyName.setPlaceholderText("Nom de famille")
        layout.addWidget(self.familyName)
        self.prenom = qtw.QLineEdit(self)
        self.prenom.setPlaceholderText("Prénom")
        layout.addWidget(self.prenom)
        self.button = qtw.QPushButton("Ajouter", self)
        self.button.clicked.connect(self.setAdd)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setAdd(self):
        Client.addClient(self.familyName.text(),self.prenom.text())
        self.close()

class DelClient(qtw.QDialog):
    def __init__(self, parent) -> None:
        super(DelClient, self).__init__()
        self.parent = parent
        layout = qtw.QVBoxLayout()
        self.lineEdit = qtw.QLineEdit(self)
        completer = qtw.QCompleter(Client.clientList(None), self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)
        #lineEdit.textChanged.connect(self.test)
        layout.addWidget(self.lineEdit)
        self.button = qtw.QPushButton("Supprimer", self)
        self.button.clicked.connect(self.setDel)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setDel(self):
        data = self.lineEdit.text().split(" ")
        Client.delClient(data[0],data[1])
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

        self.lineEdit = qtw.QLineEdit(self)
        completer = qtw.QCompleter(Client.clientList(None), self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

        self.labelPrice = qtw.QLabel()
        self.labelPrice.setText(Cart.totalPriceCart(self.cart))

        self.comboBoxPayWay = qtw.QComboBox()
        self.comboBoxPayWay.addItems({"Lydia","Espece"})

        self.quantity = qtw.QLineEdit(self)
        self.quantity.setPlaceholderText("Quantité")

        self.button = qtw.QPushButton("Ajouter au panier", self)
        self.button.clicked.connect(self.newItems)

        self.buttonValidate = qtw.QPushButton("Valider le panier",self)
        self.buttonValidate.clicked.connect(self.validateCart)

        self.myLayout.addWidget(self.productSell)
        self.layouts[1].addWidget(self.productSelect)
        self.layouts[1].addWidget(self.quantity)
        self.layouts[1].addWidget(self.button)
        self.layouts[2].addWidget(self.lineEdit)
        self.layouts[3].addWidget(self.labelPrice)
        self.layouts[3].addWidget(self.comboBoxPayWay)
        
        for k in range(0,3):
            self.myLayout.addLayout(self.layouts[3-k])
            
        self.myLayout.addWidget(self.buttonValidate)
        self.setLayout(self.myLayout)
        
    def newItems(self):
        if isfloat(self.quantity.text()) and float(self.quantity.text()) >= 0:
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
        self.familyName, self.name = self.lineEdit.text().split(" ") 
        if self.name != '' and self.familyName != '':
            DaySell.addCart(self.cart, self.familyName,self.name,self.comboBoxPayWay.currentText(),self.parent.date)
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
        self.mylayout.addWidget(self.model)
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
        client_action[0].triggered.connect(self.addClient)
        client_action[0].setShortcut("Ctrl+O")
        client_action[1] = qtw.QAction("Supprimer Client", self)
        client_action[1].triggered.connect(self.delClient)

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

    def addClient(self):
        if self.connected == True:
            wid = AddClient(self)
            wid.exec()
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()
    
    def delClient(self):
        if self.connected == True:
            wid = DelClient(self)
            wid.exec()
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    
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
        fileName = str(self.time.tm_year) + '-' + str(self.time.tm_mon) + '-' + str(self.time.tm_mday)

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

        
class TableModel(qtw.QTableWidget):
    def __init__(self, data,headerName):        # Paramétrage général        # Paramétrage général
        super(TableModel, self).__init__()
        self.setColumnCount(len(data[0]))
        self.setRowCount(len(data))
        self.setHorizontalHeaderLabels(headerName)

        for k in range(len(data)):
            for i in range(len(data[0])):
                item = qtw.QLabel()
                item.setText(data[k][i])
                
                self.setCellWidget(k,i,item)
        

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

