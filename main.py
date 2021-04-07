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
        self.scale = 8
        self.lat = '35.5'
        self.lon = '55.50'
        pic = get_pic_bytes('35.5 55.50', self.scale)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(pic)
        self.picture.setPixmap(self.pixmap)
        self.search.clicked.connect(self.search_logic)
        self.clear.clicked.connect(self.clear_logic)


    def search_logic(self):
        address = self.inf.text()
        self.lat = self.latitude.text()
        self.lon = self.longitude.text()
        try:
            pic = get_pic_bytes(self.lat + ' ' + self.lon, self.scale)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)
        except Exception:
            self.lat = '35.5'
            self.lon = '55.50'
            self.latitube.clear()
            self.longitube.clear()

    def clear_logic(self):
        self.latitube.clear()
        self.longitube.clear()
        self.inf.clear()

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_PageUp:
            if self.scale > 1:
                self.scale -= 1
            pic = get_pic_bytes(self.lat + ' ' + self.lon, self.scale)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_PageDown:
            if self.scale < 18:
                self.scale += 1
            pic = get_pic_bytes(self.lat + ' ' + self.lon, self.scale)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_Left:
            x = float(self.lat)
            y = float(self.lon) - 360 / (4 ** self.scale)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_Right:
            x = float(self.lat)
            y = float(self.lon) + 360 / (4 ** self.scale)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_Up:
            x = float(self.lat) - 180 / (4 ** self.scale)
            y = float(self.lon)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_Down:
            x = float(self.lat) + 180 / (4 ** self.scale)
            y = float(self.lon)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)


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