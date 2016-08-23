from sys import exit, argv
from PyQt5.QtWidgets import QApplication
from core.main import MainWindow
from core.version import version_number as ver

#Start Pyslvs
if __name__=="__main__":
    print("[Pyslvs "+ver+"]")
    app = QApplication(argv)
    run  = MainWindow()
    run.show()
    exit(app.exec())
