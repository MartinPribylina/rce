import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QScreen
from .main_menu import MainMenu
from .create_dataset_screen import CreateDatasetScreen
from .train_network_screen import TrainNetworkScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RCE Network Demo")
        self.setGeometry(0, 0, 800, 600)
        self.center_on_screen()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_menu = MainMenu(self.switch_screen)
        self.create_dataset_screen = CreateDatasetScreen(self.switch_screen)
        self.train_network_screen = TrainNetworkScreen(self.switch_screen)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.create_dataset_screen)
        self.stack.addWidget(self.train_network_screen)

        self.switch_screen("main_menu")

    def center_on_screen(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def switch_screen(self, screen_name):
        if screen_name == "main_menu":
            self.stack.setCurrentWidget(self.main_menu)
        elif screen_name == "create_dataset":
            self.stack.setCurrentWidget(self.create_dataset_screen)
        elif screen_name == "train_network":
            self.stack.setCurrentWidget(self.train_network_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
