import sys
import traceback
from PyQt5.QtWidgets import QMessageBox, QApplication
from gui_welcome import WelcomeWindow

def handle_exception(exc_type, exc_value, exc_traceback):
    """
    全局异常处理函数：捕获未处理的异常并弹出错误窗口
    """
    # 格式化异常信息
    exception_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # 显示错误窗口
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("程序异常")
    msg.setText(f"程序运行时发生错误：\n{str(exc_value)}")
    msg.setDetailedText(exception_details)  # 显示完整堆栈跟踪
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

# 将自定义异常处理函数挂载到全局异常处理
sys.excepthook = handle_exception

# 创建应用程序实例
if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())

