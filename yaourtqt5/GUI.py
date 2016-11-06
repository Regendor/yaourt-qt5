#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QAction, QLabel, QToolBar, QProgressBar, QVBoxLayout, QScrollArea, QMainWindow, QMenu, QSystemTrayIcon, QDesktopWidget, QMessageBox, QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication, QTimer, QThread, Qt
import os
from yaourtqt5 import YaourtWrapper


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QMenu(parent)
        openAction = menu.addAction('Open Menu')
        exitAction = menu.addAction('Exit')
        openAction.triggered.connect(self.open_main)
        exitAction.triggered.connect(self.quit)
        self.setContextMenu(menu)
        self.setToolTip('System Update')

    def open_main(self):
        self.MainWindow = MainWindow()

    def quit(self):
        if os.path.exists('guitemp.txt'):
            os.remove('guitemp.txt')
        sys.exit(0)


class UpdateThread(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        YaourtWrapper.Update()

class CenterWidget(QWidget):
    def __init__(self):
        super(CenterWidget, self).__init__()
        self.initUI()
    def initUI(self):

        self.pbr = QProgressBar()

        self.lbl = QLabel(self)
        self.scrl = QScrollArea()
        self.scrl.setWidget(self.lbl)
        self.lbl.setText('')
        self.lbl.adjustSize()

        vbox = QVBoxLayout()
        vbox.addWidget(self.scrl)
        vbox.addWidget(self.pbr)

        self.setLayout(vbox)

        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 9))

        # self.pbr = QProgressBar()
        # self.pbrd = QDockWidget()
        # self.pbrd.setWidget(self.pbr)
        # self.addDockWidget(Qt.BottomDockWidgetArea, self.pbrd)

        self.cwidget = CenterWidget()
        self.setCentralWidget(self.cwidget)

        self.setToolTip('This is a <b>QWidget</b> widget')

        if not os.path.exists('guitemp.txt'):
            self.cwidget.pbr.hide()

        self.statusBar().showMessage('Ready')

        # btn = QPushButton('Quit', self)
        # btn.clicked.connect(QCoreApplication.instance().quit)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.move(210, 160)

        UpdateAction = QAction(QIcon('Arch-linux-logo.png'), '&Start Update', self)
        UpdateAction.setShortcut('Ctrl+U')
        UpdateAction.setStatusTip('Update System')
        UpdateAction.triggered.connect(self.startUpdate)

        exitAction = QAction(QIcon('Arch-linux-logo.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.quitApp)

        self.toolbar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.toolbar.addAction(UpdateAction)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(600, 600, 600, 400)
        self.center()
        self.setWindowTitle('Arch Updater (yaourt)')
        self.setWindowIcon(QIcon('Arch-linux-logo.png'))
        # if not SystemTrayIcon(QIcon('Arch-linux-logo.png')).isVisible():
        #     self.tray_icon = SystemTrayIcon(QIcon('Arch-linux-logo.png'), self)
        #     self.tray_icon.show()

        self.labeltimer = QTimer(self)
        self.labeltimer.timeout.connect(self.onChanged)
        self.labeltimer.start(100)

        self.show()

    def startUpdate(self):
        self.updateThread = UpdateThread()
        self.updateThread.start()
        self.cwidget.pbr.show()

    def onChanged(self):
        if os.path.exists('guitemp.txt'):
            guitemp = open('guitemp.txt')
            self.cwidget.lbl.setText(guitemp.read())
            self.cwidget.lbl.adjustSize()
            if self.updateThread.isFinished():
                self.cwidget.pbr.hide()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if os.path.exists('guitemp.txt'):
                os.remove('guitemp.txt')
            event.ignore()
            self.hide()
            # event.accept()
        else:
            event.ignore()

    def quitApp(self):
        if os.path.exists('guitemp.txt'):
            os.remove('guitemp.txt')
        QCoreApplication.instance().quit()


def SysTrayStart():
    app = QApplication(sys.argv)
    tray_icon = SystemTrayIcon(QIcon('Arch-linux-logo.png'))
    tray_icon.show()
    sys.exit(app.exec_())


def MainWindowStart():
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())

def startBoth():
    app = QApplication(sys.argv)
    mw = MainWindow()
    tray_icon = SystemTrayIcon(QIcon('Arch-linux-logo.png'))
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
   MainWindowStart()