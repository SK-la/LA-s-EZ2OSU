import asyncio
import pathlib
import urllib.parse

from PyQt6 import QtWidgets

from bin.Dispatch_file import process_file


class HomeTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # 文件夹结构树
        self.input_tree = FileTreeWidget(self, "input", parent)
        self.input_tree.setHeaderLabel("输入文件夹结构")
        self.output_tree = FileTreeWidget(self, "output", parent)
        self.output_tree.setHeaderLabel("输出文件夹结构")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        tree_layout = QtWidgets.QHBoxLayout()
        tree_layout.addWidget(self.input_tree)
        tree_layout.addWidget(self.output_tree)

        layout.addLayout(tree_layout)
        self.setLayout(layout)

    # async def start_conversion(self):
    #     input_path = urllib.parse.unquote_plus(self.parent.input_path.text())
    #     output_path = self.parent.output_path.text()
    #     settings = self.parent.get_conversion_settings()
    #     cache_folder = pathlib.Path("hash_cache")
    #
    #     await start_conversion(input_path, output_path, settings, cache_folder)
    #     self.parent.show_conversion_complete_notification()

class FileTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent, tree_type, main_window):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.tree_type = tree_type
        self.main_window = main_window

    def populate_tree(self, folder_path):
        self.clear()
        root = QtWidgets.QTreeWidgetItem(self, [str(folder_path)])
        self.add_tree_items(root, folder_path)
        if self.tree_type == "input":
            self.expandToDepth(0)
        else:
            self.expandToDepth(0)  # 默认只展开一级文件夹

    def add_tree_items(self, parent_item, folder_path):
        items = sorted(folder_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for item in items:
            # 处理特殊字符
            item_name = urllib.parse.unquote(item.name)
            if item.is_dir():
                dir_item = QtWidgets.QTreeWidgetItem(parent_item, [item_name])
                self.add_tree_items(dir_item, item)
            else:
                QtWidgets.QTreeWidgetItem(parent_item, [item_name])

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
                    self.main_window.input_path.setText(str(path))
                elif self.tree_type == "output":
                    self.main_window.output_path.setText(str(path))

    def contextMenuEvent(self, event):
        item = self.itemAt(event.position().toPoint())
        if item:
            menu = QtWidgets.QMenu(self)
            if self.tree_type == "input":
                convert_action = menu.addAction("转换")
                convert_action.triggered.connect(lambda: asyncio.create_task(self.convert_file(item)))
            elif self.tree_type == "output":
                delete_action = menu.addAction("删除")
                delete_action.triggered.connect(lambda: self.delete_file(item))
            menu.exec(event.globalPos())

    async def convert_file(self, item):
        file_path = pathlib.Path(item.text(0))
        if file_path.exists() and file_path.is_file():
            output_path = pathlib.Path(self.main_window.output_path.text())
            await process_file(
                file_path, output_path, self.main_window.settings, [])
            self.main_window.show_notification(f"文件 {file_path} 转换完成")

    def delete_file(self, item):
        file_path = pathlib.Path(item.text(0))
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            self.populate_tree(file_path.parent)
