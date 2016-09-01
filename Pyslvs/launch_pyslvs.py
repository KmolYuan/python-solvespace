from sys import exit, argv
from PyQt5.QtWidgets import QApplication
from core.main import MainWindow
from core.info.version import version_number as ver

#Start Pyslvs
#Use Argument "-mpl" to build Graph Canvas by matplotlib.
if __name__=="__main__":
    print("[Pyslvs "+ver+"]")
    app = QApplication(argv)
    run  = MainWindow()
    run.show()
    exit(app.exec())
