import sys
from PyQt5.QtWidgets import QApplication, QWidget


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.ini_ui()

    def ini_ui(self):
        self.setWindowTitle('torch')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())


