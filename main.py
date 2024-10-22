import sys
from PyQt5.QtWidgets import QApplication
from gui_module import WelcomeWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 启动欢迎界面
    welcome_window = WelcomeWindow()
    welcome_window.show()

    sys.exit(app.exec_())
