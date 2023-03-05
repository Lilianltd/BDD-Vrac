from PySide6 import QtWidgets as qtw
from PySide6.QtCore import Qt, Slot
from PySide6 import QtGui as qtg
import time
from Client import Client
from Stock import Stock
from Cart import Cart
from DaySell import DaySell



#Ui of Vente

class MainVenteWidget(qtw.QWidget):
    
    def __init__(self):
        super(MainVenteWidget, self).__init__()

    def addTable(self,date):
        self.date = date
        self.mylayout = qtw.QVBoxLayout()
        self.output = qtw.QTableView()
        self.model = TableModel(DaySell.tableExtract(self.date),["Produits","Quantité","Nombre clients"])
        self.mylayout.addWidget(self.model)
        self.setLayout(self.mylayout)

    def tableActualisation(self):
        layout_Table = self.mylayout.itemAt(0)
        layout_Table.widget().deleteLater()
        self.output = qtw.QTableView()
        print(self.date)
        self.model = TableModel(DaySell.tableExtract(self.date),["Produits","Quantité","Nombre clients"])
        self.mylayout.insertWidget(0,self.model,0)
        self.setLayout(self.mylayout)

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

        self.productSelect = qtw.QComboBox(self)
        self.productSelect.setPlaceholderText("Produits")
        self.productSelect.addItems(self.products)

        self.lineEdit = qtw.QLineEdit(self)
        completer = qtw.QCompleter(Client.clientList(None), self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

        self.labelPrice = qtw.QLabel()
        self.labelPrice.setText("Total : " + str(Cart.totalPriceCart(self.cart)) + " €")

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
                self.labelPrice.setText("Total : " + str(Cart.totalPriceCart(self.cart)) + " €")
                layout_Table = self.myLayout.itemAt(0)
                layout_Table.widget().deleteLater()
                self.model = TableModel(self.cart.cart,["Produits","Quantité","Prix"])
                self.myLayout.insertWidget(0,self.model,0)
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

class MainWinMar(qtw.QMainWindow):

    def __init__(self, parent):
        self.windows = []
        super(MainWinMar, self).__init__()
        self.parent = parent
        # Création des widgets

        # Création de la fenêtre et de son pourtour
        self.mainMenu = self.menuBar()

        self.menu = [None for i in range(2)]
        self.menu[0] = self.mainMenu.addMenu("&Vente")

        self.menu[1] = self.mainMenu.addAction("Connexion")
        self.menu[1].triggered.connect(self.connexion)


        vente_action = [None,None,None]
        vente_action[0] = qtg.QAction("Accéder à un jour", self)
        vente_action[0].triggered.connect(self.accessPreviousDay)
        vente_action[1] = qtg.QAction("Vente jour actuel", self)
        vente_action[1].triggered.connect(self.createNewDay)
        vente_action[2] = qtg.QAction("Extraire au format csv", self)
        vente_action[2].triggered.connect(self.extracttocsv)

        for act in vente_action:
            self.menu[0].addAction(act)
        

        self.tabWidget = qtw.QTabWidget()
        self.resumeProductTab = MainVenteWidget()
        self.resumeClientTab = qtw.QDialog()

        self.setCentralWidget(self.tabWidget)

        self.tabWidget.addTab(self.resumeProductTab, "Résumé par produit")
        self.tabWidget.addTab(self.resumeClientTab, "Résumé par Client")

        self.buttonNewClient = qtw.QPushButton()
        self.buttonNewClient.setText("Nouveau Client")
        self.buttonNewClient.clicked.connect(self.newClient)

        statusBar = self.statusBar()
        statusBar.addWidget(self.buttonNewClient)
   
    @Slot()
    
    def connexion(self):
        if self.parent.connected == True:
            self.createNewDay()
        else:    
            self.parent.setUpConnexion()

    def createNewDay(self):
        self.time = time.gmtime()
        fileName = str(self.time.tm_year) + '-' + str(self.time.tm_mon) + '-' + str(self.time.tm_mday)
        self.date = fileName
        if self.parent.connected == True:
            self.resumeProductTab.addTable(fileName)
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def accessPreviousDay(self):
        self.date = ''
        wid = DialogChooseSell(self)
        wid.exec_()
        if self.parent.connected == True:
            self.resumeProductTab.date = self.date
            self.resumeProductTab.tableActualisation()
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()
        
    def extracttocsv(self):
        self.date = ''
        wid = DialogChooseSell(self)
        wid.exec_()
        DaySell.csvExtract(self.date)

    def tableActualisation(self):
        self.resumeProductTab.date = self.date
        self.resumeProductTab.tableActualisation()

    def newClient(self):
        self.windows.append([])
        self.windows[-1].append([])
        self.windows[-1].append(NewClient(self))
        self.windows[-1][1].show()
        

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
        if data != []:
            self.setColumnCount(len(data[0]))
            self.setRowCount(len(data))
            self.setHorizontalHeaderLabels(headerName)

            for k in range(len(data)):
                for i in range(len(data[0])):
                    item = qtw.QLabel()
                    item.setText(str(data[k][i]))
                    
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


def isfloat(value) -> bool:
  try:
    float(value)
    return True
  except ValueError:
    return False      