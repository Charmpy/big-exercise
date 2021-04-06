import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5 import uic
from search import get_pic_bytes
from PyQt5 import QtCore


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('ui.ui', self)
        pic = get_pic_bytes('35.5 55.50')
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(pic)
        self.picture.setPixmap(self.pixmap)
        self.search.clicked.connect(self.search_logic)
        self.clear.clicked.connect(self.clear_logic)

    def search_logic(self):
        address = self.inf.text()
        lat = self.latitude.text()
        lon = self.longitude.text()
        try:
            pic = get_pic_bytes(lat + ' ' + lon)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)
        except Exception:
            self.latitube.clear()
            self.longitube.clear()

    def clear_logic(self):
        self.latitube.clear()
        self.longitube.clear()
        self.inf.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.coord('l')
            self.label.move(self.x, self.y)
        elif event.key() == Qt.Key_Right:
            self.coord('r')
            self.label.move(self.x, self.y)
        if event.key() == Qt.Key_Up:
            self.coord('u')
            self.label.move(self.x, self.y)
        if event.key() == Qt.Key_Down:
            self.coord('d')
            self.label.move(self.x, self.y)

    def coord(self, key):
        if key == 'l':
            if self.x - 10 > 0:
                self.x -= 10
            else:
                self.x = 475
        elif key == 'r':
            if self.x + 10 < 475:
                self.x += 10
            else:
                self.x = 0
        elif key == 'u':
            if self.y - 10 > 0:
                self.y -= 10
            else:
                self.y = 475
        elif key == 'd':
            if self.y + 10 < 475:
                self.y += 10
            else:
                self.y = 0


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = App()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())