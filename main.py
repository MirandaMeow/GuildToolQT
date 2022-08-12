import sys

from PyQt6 import QtWidgets

import Window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Window.Window()
    ui.run()
    sys.exit(app.exec())
