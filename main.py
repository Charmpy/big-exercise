import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QButtonGroup
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

        self.type = 'map'

        self.obj = '0.0 0.0'
        rez = get_pic_bytes('35.5 55.50', self.scale, self.type, self.obj)
        self.text.setEnabled(False)

        pic = rez[0]
        self.obj = rez[2]
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(pic)
        self.picture.setPixmap(self.pixmap)
        self.search.clicked.connect(self.search_logic)
        self.clear.clicked.connect(self.clear_logic)
        self.orientation.stateChanged.connect(self.change_toggle)

        self.map.setChecked(True)

        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.map, 1)
        self.btn_group.addButton(self.sat, 2)
        self.btn_group.addButton(self.uni, 3)

        self.btn_group.buttonClicked.connect(self.radio_group)
        self.clear.clicked.connect(self.clear_logic)


    def radio_group(self, button):
        if self.map.isChecked():
            self.type = 'map'
        elif self.uni.isChecked():
            self.type = 'sat,skl'
        else:
            self.type = 'sat'
        pic = get_pic_bytes(self.lat + ' ' + self.lon, self.scale, self.type, self.obj, search=False)[0]
        self.pixmap.loadFromData(pic)
        self.picture.setPixmap(self.pixmap)

    def change_toggle(self, state):
        if state == QtCore.Qt.Checked:
            self.inf.setEnabled(False)

            self.search.setEnabled(False)
            self.sat.setEnabled(False)
            self.map.setEnabled(False)
            self.uni.setEnabled(False)
            self.clear.setEnabled(False)
        else:
            self.inf.setEnabled(True)

            self.search.setEnabled(True)
            self.sat.setEnabled(True)
            self.map.setEnabled(True)
            self.uni.setEnabled(True)
            self.clear.setEnabled(True)

    def search_logic(self):
        address = self.inf.text()
        # self.lat = self.latitude.text()
        # self.lon = self.longitude.text()
        if bool(address):
            rez = get_pic_bytes(address, self.scale, self.type, self.obj, search=True)
            self.obj = rez[2]
            pic = rez[0]
            self.text.setText(rez[3])
            self.lat,  self.lon = rez[1].split()

            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)

    def clear_logic(self):
        self.inf.clear()
        self.obj = '0.0 0.0'
        pic = get_pic_bytes(self.lat + ' ' + self.lon, self.scale, self.type, self.obj, search=False)[0]
        self.pixmap.loadFromData(pic)
        self.picture.setPixmap(self.pixmap)
        self.text.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.scale < 18:
                self.scale += 1
            pic = get_pic_bytes(self.lat + ' ' + self.lon, self.scale, self.type, self.obj, search=False)[0]
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)

        elif event.key() == Qt.Key_PageDown:
            if self.scale > 1:
                self.scale -= 1
            pic = get_pic_bytes(self.lat + ' ' + self.lon, self.scale, self.type, self.obj, search=False)[0]
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)

        elif event.key() == Qt.Key_Left:
            x = float(self.lat) - 720 / (2 ** self.scale)
            y = float(self.lon)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale, self.type, self.obj, search=False)[0]
            self.lat = str(x)
            self.lon = str(y)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)

        elif event.key() == Qt.Key_Right:
            x = float(self.lat) + 720 / (2 ** self.scale)
            y = float(self.lon)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale, self.type, self.obj, search=False)[0]
            self.lat = str(x)
            self.lon = str(y)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)

        elif event.key() == Qt.Key_Up:
            x = float(self.lat)
            y = float(self.lon) + 360 / (2 ** self.scale)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale, self.type, self.obj, search=False)[0]
            self.lat = str(x)
            self.lon = str(y)
            self.pixmap.loadFromData(pic)
            self.picture.setPixmap(self.pixmap)

        elif event.key() == Qt.Key_Down:
            x = float(self.lat)
            y = round(float(self.lon) - 360 / (2 ** self.scale), 8)
            pic = get_pic_bytes(str(x) + ' ' + str(y), self.scale, self.type, self.obj, search=False)[0]
            self.lat = str(x)
            self.lon = str(y)
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