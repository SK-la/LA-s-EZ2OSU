from PyQt5 import QtWidgets, QtGui, QtCore
import ui.ui_styling  # 导入美化脚本

class ClmTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        # 顶部文字说明和下拉框
        top_controls_layout = QtWidgets.QHBoxLayout()
        
        # 左侧下拉框组
        left_group = QtWidgets.QVBoxLayout()
        left_label = QtWidgets.QLabel("转换前的K数")
        self.k_before_combo = QtWidgets.QComboBox()
        self.k_before_combo.addItems([str(i) for i in range(1, 17)])  # 1K到16K
        self.k_before_combo.currentIndexChanged.connect(self.update_top_layout)
        left_group.addWidget(left_label)
        left_group.addWidget(self.k_before_combo)
        
        # 中间 "to" 文字
        to_label = QtWidgets.QLabel("to")
        to_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # 右侧下拉框组
        right_group = QtWidgets.QVBoxLayout()
        right_label = QtWidgets.QLabel("转换后的K数")
        self.k_after_combo = QtWidgets.QComboBox()
        self.k_after_combo.addItems([str(i) for i in range(1, 17)])  # 1K到16K
        self.k_after_combo.currentIndexChanged.connect(self.update_bottom_layout)
        right_group.addWidget(right_label)
        right_group.addWidget(self.k_after_combo)
        
        top_controls_layout.addLayout(left_group)
        top_controls_layout.addWidget(to_label)
        top_controls_layout.addLayout(right_group)

        # 上下两个等高的窗口
        self.top_widget = QtWidgets.QWidget()
        self.bottom_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QHBoxLayout(self.top_widget)
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_widget)

        layout.addLayout(top_controls_layout)
        layout.addWidget(self.top_widget)
        layout.addWidget(self.bottom_widget)

        self.setLayout(layout)

    def update_top_layout(self):
        k = int(self.k_before_combo.currentText())
        self.top_layout = self.create_k_layout(k, self.top_layout)

    def update_bottom_layout(self):
        k = int(self.k_after_combo.currentText())
        self.bottom_layout = self.create_k_layout(k, self.bottom_layout)

    def create_k_layout(self, k, layout):
        # 清空当前布局
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        # 添加K个小方块
        for i in range(k):
            line_edit = DraggableLineEdit(str(i))
            line_edit.positionChanged.connect(self.handle_position_change)
            layout.addWidget(line_edit)

        return layout

    def handle_position_change(self, text, position):
        print(f"Text: {text}, Position: {position}")

class DraggableLineEdit(QtWidgets.QWidget):
    positionChanged = QtCore.pyqtSignal(str, int)

    def __init__(self, text='', parent=None):
        super().__init__(parent)
        self.initUI(text)

    def initUI(self, text):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.line_edit = QtWidgets.QLineEdit(text)
        self.line_edit.setReadOnly(True)
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)  # 数字居中显示
        self.line_edit.setStyleSheet(ui.ui_styling.line_edit_style)  # 应用样式
        self.line_edit.mouseDoubleClickEvent = self.enable_editing
        self.line_edit.focusOutEvent = self.disable_editing

        self.drag_area = QtWidgets.QFrame()
        self.drag_area.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.drag_area.setFixedHeight(20)
        self.drag_area.setStyleSheet(ui.ui_styling.drag_area_style)  # 应用样式
        self.drag_area.mousePressEvent = self.mousePressEvent
        self.drag_area.mouseMoveEvent = self.mouseMoveEvent

        layout.addWidget(self.line_edit)
        layout.addWidget(self.drag_area)
        self.setLayout(layout)

    def enable_editing(self, event):
        self.line_edit.setReadOnly(False)

    def disable_editing(self, event):
        self.line_edit.setReadOnly(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return

        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        mime_data.setText(self.line_edit.text())
        drag.setMimeData(mime_data)
        drag.exec_(QtCore.Qt.MoveAction)

    def dropEvent(self, event):
        if event.source() == self:
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            self.positionChanged.emit(self.line_edit.text(), self.pos())
        else:
            event.ignore()
