from PySide6 import QtWidgets as qtw
from PySide6.QtCore import Qt, Slot
from PySide6 import QtGui as qtg
import time

from Client import Client
from Stock import Stock
from Cart import Cart
from DaySell import DaySell

#Ui of Vente

class resumeProduct(qtw.QWidget):
    
    def __init__(self,parent):
        super(resumeProduct, self).__init__()
        self.parent = parent
        self.mylayout = qtw.QVBoxLayout()

        self.model = TableModel([],["Produits","Quantité","Nombre clients"])
        self.mylayout.addWidget(self.model)
        self.setLayout(self.mylayout)

    def tableActualisation(self):
        self.date = self.parent.date
        layout_Table = self.mylayout.itemAt(0)
        layout_Table.widget().deleteLater()
        self.output = qtw.QTableView()
        self.model = TableModel(DaySell.tableExtract(self.parent.date),["Produits","Quantité","Nombre clients"])
        self.mylayout.insertWidget(0,self.model,0)
        self.setLayout(self.mylayout)

class resumeClient(qtw.QWidget):
    
    def __init__(self,parent):
        super(resumeClient, self).__init__()
        self.parent = parent
        self.mylayout = qtw.QVBoxLayout()
        self.output = qtw.QTableView()
        self.model = TableModel([],["Produits","Quantité","Nombre clients"])
        self.mylayout.addWidget(self.model)
        self.setLayout(self.mylayout)

    def tableActualisation(self):
        
        self.date = self.parent.date
        layout_Table = self.mylayout.itemAt(0)
        layout_Table.widget().deleteLater()
        self.output = qtw.QTableView()
        self.data = DaySell.clientExtract(self.parent.date)
        self.parent.totalEspece.setText("Total espèce: " + str(round(self.data[1]*100)/100) +" €")
        self.parent.totalLydia.setText("Total lydia : " + str(round(self.data[2]*100)/100) +" €")
        self.model = TableModel(self.data[0],["Nom","Prenom","Total","Moyens"])
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
        self.model = TableModelCart(self.cart.cart,["Produits","Quantité","Prix"],self)

        self.productSelect = qtw.QComboBox(self)
        self.productSelect.setPlaceholderText("Produits")
        self.productSelect.addItems(self.products)

        self.lineEdit = qtw.QLineEdit(self)
        completer = qtw.QCompleter(Client.clientList(None), self)
        completer.setFilterMode(Qt.MatchContains)
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

        if isfloat(self.quantity.text()) and float(self.quantity.text()) >= 0: #on check si les données sont conformes à ce qu'on attend (prix flottant et positif)
            idachat = self.cart.productIndex(self.productSelect.currentText()) 

            if idachat == -1: #on check si dans le panier le produit existe déjà
                if Stock.isProductAvailable(self.productSelect.currentText(),float(self.quantity.text())):
                    Cart.addProduct(self.cart, self.productSelect.currentText(), float(self.quantity.text()))
                    self.actualise()
                else:
                    self.check = None
                    widerror = NegativeStock(self)
                    widerror.exec_()
                    if self.check == True:
                        Cart.addProduct(self.cart, self.productSelect.currentText(), float(self.quantity.text()))
                        self.actualise()

            else: #l'item existe déjà dans le panier on va devoir modifier la quantité du panier
                oldQuantity = self.cart.cart[idachat][1]
                if Stock.isProductAvailable(self.productSelect.currentText(),float(self.quantity.text())+oldQuantity):
                    self.cart.removeProduct(self.productSelect.currentText())
                    Cart.addProduct(self.cart, self.productSelect.currentText(), float(self.quantity.text())+oldQuantity) 
                    self.actualise()
                else:
                    self.check = None
                    widerror = NegativeStock(self)
                    widerror.exec_()
                    if self.check == True:
                        self.cart.removeProduct(self.productSelect.currentText())
                        Cart.addProduct(self.cart, self.productSelect.currentText(), float(self.quantity.text())+oldQuantity) 
                        self.actualise()
        else:
            self.quantity.setText("")
            widerror = ErrorMessage("Format invalid")
            widerror.exec_()
            
    def actualise(self):
        self.labelPrice.setText("Total : " + str(Cart.totalPriceCart(self.cart)) + " €")
        layout_Table = self.myLayout.itemAt(0)
        layout_Table.widget().deleteLater()
        self.model = TableModelCart(self.cart.cart,["Produits","Quantité","Prix"],self)
        self.myLayout.insertWidget(0,self.model,0)
        self.setLayout(self.myLayout)
        self.quantity.setText("")

    def validateCart(self):
        if self.lineEdit.text() == "":
            widerror = ErrorMessage("Enter a Family name and a name")
            widerror.exec_()
        else:
            self.familyName, self.name = self.lineEdit.text().split(" ")
            if self.name != '' and self.familyName != '':
                DaySell.addCart(self.cart, self.familyName,self.name,self.comboBoxPayWay.currentText(),self.parent.date)
                self.parent.tableActualisation()
                self.close()
            else:
                widerror = ErrorMessage("Enter a Family name and a name")
                widerror.exec_()

class TableModel(qtw.QTableWidget):
    def __init__(self, data,headerName):        # Paramétrage général        # Paramétrage général
        super(TableModel, self).__init__()
        self.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        if data != []:
            self.setColumnCount(len(data[0]))
            self.setRowCount(len(data))
            self.setHorizontalHeaderLabels(headerName)

            for k in range(len(data)):
                for i in range(len(data[0])):                    
                    self.setItem(k, i, qtw.QTableWidgetItem(str(data[k][i])))
        self.setSizeAdjustPolicy(qtw.QTableWidget.AdjustToContents)

class NegativeStock(qtw.QDialog):
    def __init__(self,parent):
        self.parent = parent
        super(NegativeStock, self).__init__()
        self.setWindowTitle("Erreur")
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QLabel()
        self.productName.setText("Attention stock négatif, valider vous tout de même ?")
        layout.addWidget(self.productName)
        layout2 = qtw.QHBoxLayout()

        self.buttonOui = qtw.QPushButton()
        self.buttonOui.setText("Oui")
        self.buttonOui.clicked.connect(self.oui)

        self.buttonNon = qtw.QPushButton()
        self.buttonNon.setText("Non")
        self.buttonNon.clicked.connect(self.non)
        layout2.addWidget(self.buttonOui)
        layout2.addWidget(self.buttonNon)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def oui(self):
        self.parent.check = True
        self.close()

    def non(self):
        self.parent.check = False
        self.close()

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
        self.resumeProductTab = resumeProduct(self)
        self.resumeClientTab = resumeClient(self)

        self.setCentralWidget(self.tabWidget)

        self.tabWidget.addTab(self.resumeProductTab, "Résumé par produit")
        self.tabWidget.addTab(self.resumeClientTab, "Résumé par Client")

        self.buttonNewClient = qtw.QPushButton()
        self.buttonNewClient.setText("Nouveau Client")
        self.buttonNewClient.clicked.connect(self.newClient)

        self.totalEspece = qtw.QLabel()
        self.totalLydia = qtw.QLabel()

        
        statusBar = self.statusBar()
        statusBar.addWidget(self.buttonNewClient)
        statusBar.addPermanentWidget(self.totalEspece)
        statusBar.addPermanentWidget(self.totalLydia)


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
            self.tableActualisation()
        else:
            wid = ErrorMessage("Connectez-vous")
            wid.exec_()

    def accessPreviousDay(self):
        self.date = ''
        wid = DialogChooseSell(self)
        wid.exec_()
        if self.parent.connected == True:
            self.tableActualisation()
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
        self.resumeClientTab.date = self.date

        self.resumeClientTab.tableActualisation()
        
        self.resumeProductTab.tableActualisation()

    def newClient(self):
        if self.parent.connected == True:
            self.windows.append([])
            self.windows[-1].append([])
            self.windows[-1].append(NewClient(self))
            self.windows[-1][1].show()
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

class TableModelCart(qtw.QTableWidget):
    def __init__(self, data : list,headerName : list, parent : NewClient):        # Paramétrage général        # Paramétrage général
        super(TableModelCart, self).__init__()
        self.parent = parent
        headerName.append(" ")
        self.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(qtw.QTableWidget.AdjustToContents)
        if data != []:
            self.setColumnCount(len(data[0])+1)
            self.setRowCount(len(data))
            self.setHorizontalHeaderLabels(headerName)
            self.myitem = []
            for k in range(len(data)):
                self.myitem.append([])
                for i in range(len(data[0])):
                    self.myitem[k].append(qtw.QTableWidgetItem(str(data[k][i])))
                    self.setItem(k, i, self.myitem[k][i])
                self.setItem(k, i+1, qtw.QTableWidgetItem("x"))
                self.cellDoubleClicked.connect(self.supp)

    def supp(self):
        row = self.currentIndex().row()
        column = self.currentIndex().column()
        productName = self.myitem[row][0].text()

        if (column+1) == self.columnCount():
            self.parent.cart.removeProduct(productName)
            self.parent.actualise()

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