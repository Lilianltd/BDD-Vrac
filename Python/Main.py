from PySide6 import QtWidgets as qtw
import sys
import StockUI
import ClientUI
import VenteUI
#Ui of Stock


class SetUpUI(qtw.QMainWindow) :
    
    def __init__(self, parent=None):
        
        super(SetUpUI, self).__init__(parent)
        
        self.tabWidget = qtw.QTabWidget()
        self.stockTab = StockUI.MainWinMar()
        self.clientTab = qtw.QMainWindow()
        self.venteTab = qtw.QWidget()
        
        self.tabWidget.addTab(self.stockTab, "Stock")
        self.tabWidget.addTab(self.venteTab, "Vente")
        self.tabWidget.addTab(self.clientTab, "Client")
          
          
        # ONGLET VISUALISATION
        # TO COMPLETE
          
        # MAIN LAYOUT
    
        self.setWindowTitle(u"BDD Vrac")
        self.resize(500, 550)
        self.setCentralWidget(self.tabWidget)

  
if __name__ ==  '__main__' :
    import sys
    app = qtw.QApplication(sys.argv)

    main = SetUpUI()
    main.show()
    sys.exit(app.exec_())