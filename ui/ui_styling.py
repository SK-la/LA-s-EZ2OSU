#ui_styling.py
import pathlib
from PyQt5 import QtGui, QtWidgets, QtCore

def set_window_icon(window):
    icon_path = pathlib.Path(__file__).parent.parent / 'ico' / 'icon.png'
    window.setWindowIcon(QtGui.QIcon(str(icon_path)))

def set_background_image(window):
    bg_path = pathlib.Path(__file__).parent.parent / 'ico' / 'bg.png'
    if not bg_path.exists():
        print(f"Background image not found at: {bg_path}")
        return

    label = QtWidgets.QLabel(window)
    pixmap = QtGui.QPixmap(str(bg_path))

    dark_pixmap = pixmap.copy()
    painter = QtGui.QPainter(dark_pixmap)
    painter.fillRect(dark_pixmap.rect(), QtGui.QColor(0, 0, 0, 120))
    painter.end()

    label.setPixmap(dark_pixmap)
    label.setScaledContents(True)
    label.setGeometry(0, 0, window.width(), window.height())
    label.setStyleSheet("background: transparent; border: none;")
    label.lower()

    def resize_event(event):
        label.setGeometry(0, 0, window.width(), window.height())
        scaled_pixmap = dark_pixmap.scaled(window.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        label.setPixmap(scaled_pixmap)
        super(window.__class__, window).resizeEvent(event)

    window.resizeEvent = resize_event

    set_stylesheet(window)

def set_stylesheet(window):
    window.setStyleSheet("""
        QWidget, QMainWindow {
            background-color: rgba(0, 0, 0, 0);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0);
        }
        QLineEdit {
            background-color: rgba(0, 0, 0, 0);
            color: white;
            border: 1px solid rgba(255, 255, 255, 50);
            text-align: center;  /* 数字居中显示 */
        }
        QComboBox {
            background-color: rgba(0, 0, 0, 0);
            color: white;
            border: 1px solid rgba(255, 255, 255, 50);
        }
        QTabWidget::pane {
            background-color: rgba(0, 0, 0, 0);
            color: white;
            border: none;
        }
        QPushButton, QTabBar::tab {
            background-color: rgba(0, 0, 0, 120);
            color: white;
            padding: 4px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: rgba(56, 120, 200, 100);
        }
        QTabWidget::tab-bar {
            alignment: center;
        }
        QTabBar::tab:selected {
            background: rgba(56, 120, 200, 120);
            color: white;
        }
        QScrollBar:vertical {
            background: rgba(0, 0, 0, 0);
            width: 15px;
            margin: 15px 3px 15px 3px;
            border: 0px solid rgba(255, 255, 255, 80);
        }
        QScrollBar::handle:vertical {
            background: rgba(56, 120, 200, 200);
            min-height: 25px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            border: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        QTreeWidget::header {
            background-color: rgba(0, 0, 0, 0);
            color: white;
            border: 1px solid rgba(255, 255, 255, 50);
        }
        QTreeWidget::header::section {
            background-color: rgba(0, 0, 0, 0);
            color: white;
            border: 1px solid rgba(255, 255, 255, 50);
        }
        QCheckBox {
            color: black;
        }
    """)

line_edit_style = """
    QLineEdit {
        border: 1px solid gray;
        border-radius: 5px;
        padding: 5px;
        background: white;
        text-align: center;  /* 数字居中显示 */
    }
"""

drag_area_style = """
    QFrame {
        background-color: lightgray;
    }
"""
