from PySide6 import QtWidgets as qtw
from PySide6.QtCore import Qt, Slot
from Client import Client


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
        completer.setFilterMode(Qt.MatchContains)
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

class MainWinMar(qtw.QMainWindow):

    def __init__(self, parent):
        super(MainWinMar, self).__init__()
        self.parent = parent
        # Création des widgets

        # Création de la fenêtre et de son pourtour
        self.mainMenu = self.menuBar()
        self.menu = [None for i in range(0,3)]

        self.menu[0] = self.mainMenu.addAction("Ajouter un client")
        self.menu[0].triggered.connect(self.addClient)
        self.menu[1] = self.mainMenu.addAction("Supprimer un client")
        self.menu[1].triggered.connect(self.delClient)
        self.menu[2] = self.mainMenu.addAction("Connexion")
        self.menu[2].triggered.connect(self.connexion)
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

class ErrorMessage(qtw.QDialog):
    def __init__(self,message):
        super(ErrorMessage, self).__init__()
        self.setWindowTitle("Erreur")
        layout = qtw.QVBoxLayout()
        self.productName = qtw.QLabel()
        self.productName.setText(message)
        layout.addWidget(self.productName)
        self.setLayout(layout)

        