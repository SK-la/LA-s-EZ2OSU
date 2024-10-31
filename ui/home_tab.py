#home_tab.py
import pathlib
from PyQt5 import QtWidgets, QtCore
from Dispatch_file import process_file

class HomeTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        
        # 文件夹结构树
        self.input_tree = FileTreeWidget(self, "input")
        self.input_tree.setHeaderLabel("输入文件夹结构")
        self.output_tree = FileTreeWidget(self, "output")
        self.output_tree.setHeaderLabel("输出文件夹结构")
        
        tree_layout = QtWidgets.QHBoxLayout()
        tree_layout.addWidget(self.input_tree)
        tree_layout.addWidget(self.output_tree)
        
        layout.addLayout(tree_layout)
        self.setLayout(layout)

    def start_conversion(self):
        self.parent.start_conversion()

class FileTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent, tree_type):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.tree_type = tree_type

    def populate_tree(self, folder_path):
        self.clear()
        root = QtWidgets.QTreeWidgetItem(self, [str(folder_path)])
        self.add_tree_items(root, folder_path)
        self.expandAll()

    def add_tree_items(self, parent_item, folder_path):
        for item in folder_path.iterdir():
            if item.is_dir():
                dir_item = QtWidgets.QTreeWidgetItem(parent_item, [item.name])
                self.add_tree_items(dir_item, item)
            else:
                QtWidgets.QTreeWidgetItem(parent_item, [item.name])

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = pathlib.Path(url.toLocalFile())
            if path.exists() and path.is_dir():
                self.populate_tree(path)
                if self.tree_type == "input":
                    self.parent().parent.input_path.setText(str(path))
                elif self.tree_type == "output":
                    self.parent().parent.output_path.setText(str(path))

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            menu = QtWidgets.QMenu(self)
            if self.tree_type == "input":
                convert_action = menu.addAction("转换")
                convert_action.triggered.connect(lambda: self.convert_file(item))
            elif self.tree_type == "output":
                delete_action = menu.addAction("删除")
                delete_action.triggered.connect(lambda: self.delete_file(item))
            menu.exec_(event.globalPos())

    def convert_file(self, item):
        file_path = pathlib.Path(item.text(0))
        if file_path.exists() and file_path.is_file():
            output_path = pathlib.Path(self.parent().parent.output_path.text())
            process_file(
                file_path, output_path, 
                self.parent().parent.include_audio.isChecked(), 
                self.parent().parent.include_images.isChecked()
            )

    def delete_file(self, item):
        file_path = pathlib.Path(item.text(0))
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            self.populate_tree(file_path.parent)
