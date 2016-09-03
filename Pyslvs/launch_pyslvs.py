from sys import exit, argv

#Start Pyslvs
#Use Argument "-mpl" to build Graph Canvas by matplotlib.
if __name__=="__main__":
    from core.info.version import show_version
    show_version()
    from PyQt5.QtWidgets import QApplication
    from core.main import MainWindow
    app = QApplication(argv)
    run  = MainWindow()
    run.show()
    exit(app.exec())
