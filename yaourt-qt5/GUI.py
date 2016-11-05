#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QAction, QTextEdit, qApp, QMainWindow, QMenu, QSystemTrayIcon, QDesktopWidget, QMessageBox, QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QMenu(parent)
        openAction = menu.addAction('Open Menu')
        exitAction = menu.addAction('Exit')
        openAction.triggered.connect(self.open_main)
        exitAction.triggered.connect(self.quit)
        self.setContextMenu(menu)

    def open_main(self):
        self.MainWindow = MainWindow()

    def quit(self):
        sys.exit(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 9))

        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        self.setToolTip('This is a <b>QWidget</b> widget')

        self.statusBar().showMessage('Ready')

        btn = QPushButton('Quit', self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(210, 160)

        exitAction = QAction(QIcon('Arch-linux-logo.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.center()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('Arch-linux-logo.png'))
        # if not SystemTrayIcon(QIcon('Arch-linux-logo.png')).isVisible():
        #     self.tray_icon = SystemTrayIcon(QIcon('Arch-linux-logo.png'), self)
        #     self.tray_icon.show()

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hide()
            # event.accept()
            event.ignore()
        else:
            event.ignore()


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
   SysTrayStart()