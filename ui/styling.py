import pathlib
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt  # 确保导入 Qt

def set_window_icon(window):
    icon_path = pathlib.Path(__file__).parent.parent / 'BGi' / 'icon.png'
    window.setWindowIcon(QtGui.QIcon(str(icon_path)))

def set_background_image(window):
    bg_path = pathlib.Path(__file__).parent.parent / 'BGi' / 'bg.png'
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
    label.setAlignment(Qt.AlignCenter)  # 使用 Qt.AlignCenter
    label.setStyleSheet("background: transparent; border: none;")
    label.lower()

    def resize_event(event):
        label.resize(window.size())
        super(QtWidgets.QMainWindow, window).resizeEvent(event)

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
        background-color: rgba(0, 0, 0, 120);
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #555;
        text-align: center;  /* 数字居中显示 */
        property-alignment: 'AlignCenter';  /* 确保居中对齐 */
    }
    QLineEdit:focus {
        border: 1px solid #00f;
        text-align: center;
        property-alignment: 'AlignCenter';  /* 确保焦点状态下居中对齐 */
    }
"""

drag_area_style = """
    QFrame {
        background-color: light-gray;
    }
"""

radio_button_style = """
    QRadioButton {
        background-color: rgba(0, 0, 0, 120);
        color: #fff;
        padding: 5px;
        border-radius: 5px;
    }
    QRadioButton::indicator {
        width: 20px;
        height: 20px;
    }
    QRadioButton::indicator::unchecked {
        background-color: rgba(0, 0, 0, 120);
        border: 1px solid #888;
    }
    QRadioButton::indicator::checked {
        background-color: rgba(56, 86, 120, 220);
        border: 1px solid #00f;
    }
"""

label_style = """
    QLabel {
        background-color: rgba(0, 0, 0, 120);
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
"""
