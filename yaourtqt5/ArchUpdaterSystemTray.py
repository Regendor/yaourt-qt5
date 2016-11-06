import sys
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, QTimer
import os
from yaourtqt5 import UpdaterBackend
from yaourtqt5 import ArchUpdaterGUI


class UpdateThread(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        UpdaterBackend.Update(noconfirm=0)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QMenu(parent)
        openAction = menu.addAction('Open Menu')
        exitAction = menu.addAction('Exit')
        openAction.triggered.connect(self.open_main)
        exitAction.triggered.connect(self.trayquit)
        self.setContextMenu(menu)
        self.setToolTip('System Update')

        self.updatechktimer = QTimer(self)
        self.updatechktimer.timeout.connect(self.YaourtQuery)
        self.updatechktimer.start(3600000)

        self.lbltimer = QTimer(self)
        self.lbltimer.timeout.connect(self.changeIcon)
        self.lbltimer.start(100)

        self.icon = QIcon('TrayUpdatedIcon.png')
        self.show()

    def YaourtQuery(self):
        self.queryThread = UpdateThread()
        self.queryThread.start()

    def open_main(self):
        self.MainWindow = ArchUpdaterGUI.MainWindow()

    def trayquit(self):
        if os.path.exists('guitemp.txt'):
            os.remove('guitemp.txt')
        sys.exit(0)

    def changeIcon(self):
        if os.path.exists('temp.txt'):
            tempf = open('temp.txt')
            tempfv = tempf.read()
            if '(Y' in tempfv:
                self.hide()
                self.icon = QIcon('TrayUpdateAvailableIcon.png')
                self.show()
            elif 'Foreign packages:' in tempfv:
                self.hide()
                self.icon = QIcon('TrayUpdatedIcon.png')
                self.show()


def SysTrayStart():
    if os.path.exists('guitemp.txt'):
        os.remove('guitemp.txt')
    if os.path.exists('downtemp.txt'):
        os.remove('downtemp.txt')
    if os.path.exists('upgrtemp.txt'):
        os.remove('upgrtemp.txt')
    if os.path.exists('temp.txt'):
        os.remove('temp.txt')
    if UpdaterBackend.processVerification('ArchUpdaterSystemTray.py') == 'running':
        mbapp = QApplication(sys.argv)
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setWindowTitle('Error')
        mb.setText('The process is already running.')
        mb.setStandardButtons(QMessageBox.Ok)
        mb.show()
        sys.exit(mbapp.exec_())
    else:
        app = QApplication(sys.argv)
        tray_iconupdated = SystemTrayIcon(QIcon('TrayUpdatedIcon.png'))
        tray_iconupdated.show()
        sys.exit(app.exec_())

SysTrayStart()
