#ui/clm_tab.py
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEvent
import ui.styling


class ClmTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_widget = None  # 在 __init__ 中定义实例属性
        self.bottom_widget = None  # 在 __init__ 中定义实例属性
        self.top_layout = None  # 在 __init__ 中定义实例属性
        self.bottom_layout = None  # 在 __init__ 中定义实例属性
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        # 顶部文字说明和点选按钮
        top_controls_layout = QtWidgets.QVBoxLayout()

        # 上排点选按钮组
        top_label = QtWidgets.QLabel("转换前的K数")
        top_controls_layout.addWidget(top_label)
        self.create_radio_buttons(top_controls_layout, self.update_top_layout)

        # 下排点选按钮组
        bottom_label = QtWidgets.QLabel("转换后的K数")
        top_controls_layout.addWidget(bottom_label)
        self.create_radio_buttons(top_controls_layout, self.update_bottom_layout)

        # 上下两个等高的窗口
        self.top_widget = QtWidgets.QWidget()
        self.bottom_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QHBoxLayout(self.top_widget)
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_widget)

        layout.addLayout(top_controls_layout)
        layout.addWidget(self.top_widget)
        layout.addWidget(self.bottom_widget)

        self.setLayout(layout)

    def create_radio_buttons(self, layout, toggle_function):
        button_group = QtWidgets.QButtonGroup(self)
        button_layout = QtWidgets.QHBoxLayout()
        for i in range(4, 19):
            button = QtWidgets.QRadioButton(str(i))
            button.setStyleSheet(ui.styling.radio_button_style)
            button.toggled.connect(toggle_function)
            button_group.addButton(button)
            button_layout.addWidget(button)
        layout.addLayout(button_layout)

    def update_top_layout(self):
        button = self.sender()
        if button.isChecked():
            k = int(button.text())
            self.top_layout = self.create_fixed_layout(k, self.top_layout)

    def update_bottom_layout(self):
        button = self.sender()
        if button.isChecked():
            k = int(button.text())
            self.bottom_layout = self.create_editable_layout(k, self.bottom_layout)

    @staticmethod
    def create_fixed_layout(k, layout):
        # 清空当前布局
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        # 添加K个固定数字的标签
        for i in range(k):
            label = QtWidgets.QLabel(str(i + 1))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(ui.styling.label_style)
            layout.addWidget(label)

        return layout

    @staticmethod
    def create_editable_layout(k, layout):
        # 清空当前布局
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        # 添加K个输入框
        for i in range(k):
            line_edit = AutoSwitchLineEdit()
            line_edit.setStyleSheet(ui.styling.line_edit_style)
            layout.addWidget(line_edit)

        return layout


class AutoSwitchLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaxLength(1)  # 每个输入框只允许输入一个字符
        self.textChanged.connect(self.switch_focus)
        self.setFocusPolicy(Qt.StrongFocus)
        self.installEventFilter(self)

    def switch_focus(self, text):
        if len(text) == 1:
            next_widget = self.nextInFocusChain()
            if isinstance(next_widget, AutoSwitchLineEdit):
                next_widget.setFocus()
                next_widget.selectAll()  # 选择所有文本以便覆盖

    def eventFilter(self, source, event):
        if event.type() == QEvent.FocusIn:
            self.selectAll()
        return super().eventFilter(source, event)
