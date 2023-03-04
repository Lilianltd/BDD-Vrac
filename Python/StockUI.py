from PySide6 import QtWidgets as qtw
from PySide6.QtCore import Qt, Slot
from PySide6 import QtGui as qtg
import time
from Client import Client
from Stock import Stock
from Cart import Cart
from DaySell import DaySell


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

class OutputStock(qtw.QWidget):
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
# 

class MainWinMar(qtw.QMainWindow):

    def __init__(self, parent):
        super(MainWinMar, self).__init__()
        self.parent = parent
        # Création des widgets

        # Création de la fenêtre et de son pourtour
        self.mainMenu = self.menuBar()

        self.menu = [None for i in range(4)]
        self.menu[0] = self.mainMenu.addMenu("&Stock")
        self.menu[1] = self.mainMenu.addMenu("&Client")
        self.menu[2] = self.mainMenu.addAction("Connexion")
        self.menu[2].triggered.connect(self.connexion)
        self.menu[3] = self.mainMenu.addMenu("&Vente")

        # Création des sous-menus pour les stocks
        stock_action = [None for i in range(4)]
        stock_action[0] = qtg.QAction("Rajouter un produit", self)
        stock_action[0].triggered.connect(self.addProduct)
        stock_action[1] = qtg.QAction("Supprimer un produit", self)
        stock_action[1].triggered.connect(self.delProduct)
        stock_action[2] = qtg.QAction("Réapprovisionner", self)
        stock_action[2].triggered.connect(self.updateStock)
        stock_action[3] = qtg.QAction("Modifier un produit", self)
        stock_action[3].triggered.connect(self.modifyProduct)

        for i in range(len(stock_action)):
            self.menu[0].addAction(stock_action[i])

        # Création des sous-menus pour les clients

        client_action = [None, None]
        client_action[0] = qtg.QAction("Nouveau Client", self)
        client_action[0].triggered.connect(self.addClient)
        client_action[0].setShortcut("Ctrl+O")
        client_action[1] = qtg.QAction("Supprimer Client", self)
        client_action[1].triggered.connect(self.delClient)

        for i in client_action:
            self.menu[1].addAction(i)


        vente_action = [None,None,None]
        vente_action[0] = qtg.QAction("Accéder à un jour", self)
        vente_action[0].triggered.connect(self.accessPreviousDay)
        vente_action[1] = qtg.QAction("Vente jour actuel", self)
        vente_action[1].triggered.connect(self.createNewDay)
        vente_action[2] = qtg.QAction("Extraire au format csv", self)
        vente_action[2].triggered.connect(self.extracttocsv)


        for act in vente_action:
            self.menu[3].addAction(act)
    @Slot()

    def addClient(self):
        if self.parent.connected == True:
            wid = AddClient(self)
            wid.exec()
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()
    
    def delClient(self):
        if self.parent.connected == True:
            wid = DelClient(self)
            wid.exec()
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    
    def connexion(self):
        self.parent.setUpConnexion()
        if self.parent.connected == True:
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)

        
    def updateStock(self):
        if self.parent.connected == True:
            wid = UpdateStock(self)
            wid.exec()
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def addProduct(self):
        if self.parent.connected == True:
            wid = AddProduct(self)
            wid.exec()
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def delProduct(self):
        if self.parent.connected == True:
            wid = DelProduct()
            wid.exec()
            self.widget = MainWinWidget(self)
            self.setCentralWidget(self.widget)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def modifyProduct(self):
        if self.parent.connected == True:
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

        if self.parent.connected == True:
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
        if self.parent.connected == True:
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