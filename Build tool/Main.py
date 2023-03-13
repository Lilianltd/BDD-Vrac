from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
import sys
import StockUI 
import ClientUI
import VenteUI
#Ui of Stock

class SetUpUI(qtw.QMainWindow) :    
    def __init__(self, parent=None):
        super(SetUpUI, self).__init__(parent)
        self.connected = False
        self.setWindowIcon(qtg.QIcon(qtg.QIcon(qtg.QPixmap("icon.png"))))
        self.tabWidget = qtw.QTabWidget()
        self.stockTab = StockUI.MainWinMar(self)
        self.clientTab = ClientUI.MainWinMar(self)
        self.venteTab = VenteUI.MainWinMar(self)
        
        self.tabWidget.addTab(self.stockTab, "Stock")
        self.tabWidget.addTab(self.venteTab, "Vente")
        self.tabWidget.addTab(self.clientTab, "Client")
        
        self.setWindowTitle(u"BDD Vrac")
        self.resize(1000, 800)
        self.setCentralWidget(self.tabWidget)

    def setUpConnexion(self):
        wid = ConnexionWidget()
        wid.exec()
        main.stockTab.connexion()
        main.venteTab.connexion()
        

class ConnexionWidget(qtw.QDialog):
    def __init__(self, box=False) -> None:
        super(ConnexionWidget, self).__init__()
        self.isBox = box
        layout = qtw.QVBoxLayout()
        self.id = qtw.QLineEdit()
        self.id.setPlaceholderText("Identifiant")
        layout.addWidget(self.id)
        self.mdp = qtw.QLineEdit(self)
        self.mdp.setEchoMode(qtw.QLineEdit.PasswordEchoOnEdit)
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
            main.connected = True
            self.close()
        else:
            self.mdp.setText("")
            self.id.setText("")

if __name__ ==  '__main__' :
    sys.argv += ['-platform', 'windows:darkmode=2']
    app = qtw.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setWindowIcon(qtg.QIcon('icon.png'))
    print(app.windowIcon())
    main = SetUpUI()
    main.show()
    main.setWindowIcon(qtg.QIcon('icon.png'))
    sys.exit(app.exec())
