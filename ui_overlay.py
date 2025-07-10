from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint, QTimer
from ai_screenshot import send_clipboard_to_gpt
import sys

class Overlay(QWidget):
    def __init__(self, auto_capture=True, delay=3):
        super().__init__()
        self.auto_capture = auto_capture
        self.delay = delay

        self.setWindowTitle("Draw Overlay")
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drawing = False
        self.last_point = QPoint()
        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.transparent)

        if self.auto_capture:
            QTimer.singleShot(self.delay * 1000, self.take_screenshot)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.canvas)
            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def show_message(self, text):
        self.toast = QLabel(text, self)
        self.toast.setStyleSheet("""
            QLabel {
                background-color: #333;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 8px;
            }
        """)
        self.toast.setAlignment(Qt.AlignCenter)
        self.toast.resize(300, 50)
        self.toast.move((self.width() - self.toast.width()) // 2,
                        (self.height() - self.toast.height()) // 2)
        self.toast.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.toast.show()
        QTimer.singleShot(1500, self.toast.close)

    def take_screenshot(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        screenshot.save("clip.png", "PNG")
        print("[INFO] Screenshot saved as clip.png")
        self.show_message("📸 Screenshot taken successfully!")
        send_clipboard_to_gpt("clip.png")
        QTimer.singleShot(1700, self.close)

def launch_overlay(auto_capture=True, delay=3):
    app = QApplication(sys.argv)
    overlay = Overlay(auto_capture=auto_capture, delay=delay)
    overlay.show()
    app.exec_()
