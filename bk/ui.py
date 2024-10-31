import pathlib
from PyQt5 import QtWidgets, QtCore, QtGui  # 添加 QtGui 模块
from Dispatch_data import process_file

class FileDropWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.names_obj = None  # Initialize names_obj
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LAs EZ2OSU')
        self.setGeometry(100, 100, 800, 600)
        
        # 设置窗口图标
        icon_path = pathlib.Path(__file__).parent / 'ico' / 'icon.png'
        self.setWindowIcon(QtGui.QIcon(str(icon_path)))

        # 设置窗口背景图片
        bg_path = pathlib.Path(__file__).parent / 'ico' / 'bg.png'
        self.setStyleSheet(f"""
            QWidget {{
                background-image: url({bg_path});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;  /* 保持比例缩放并适应填充窗口 */
            }}
        """)

        layout = QtWidgets.QVBoxLayout()
        
        self.tabs = QtWidgets.QTabWidget()
        self.home_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.home_tab, "Home")
        
        self.initHomeTab()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def initHomeTab(self):
        layout = QtWidgets.QVBoxLayout()
        
        # Input file or folder
        input_layout = QtWidgets.QHBoxLayout()
        self.input_path = QtWidgets.QLineEdit()
        self.input_path.setPlaceholderText("输入文件夹路径")
        input_button = QtWidgets.QPushButton("设置输入")
        input_button.clicked.connect(self.select_input)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(input_button)
        
        # Output file or folder
        output_layout = QtWidgets.QHBoxLayout()
        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("输出文件夹路径")
        output_button = QtWidgets.QPushButton("设置输出")
        output_button.clicked.connect(self.select_output)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(output_button)
        
        # Checkboxes
        checkbox_layout = QtWidgets.QHBoxLayout()
        self.include_audio = QtWidgets.QCheckBox("包含音频文件")
        self.include_images = QtWidgets.QCheckBox("包含图片文件")
        self.rename_output_folder = QtWidgets.QCheckBox("重命名输出文件夹")
        self.rename_output_folder.stateChanged.connect(self.rename_output_folder_checked)  # Connect checkbox state change signal
        checkbox_layout.addWidget(self.include_audio)
        checkbox_layout.addWidget(self.include_images)
        checkbox_layout.addWidget(self.rename_output_folder)
        
        # Folder structure trees
        self.input_tree = FileTreeWidget(self, "input")
        self.input_tree.setHeaderLabel("输入文件夹结构")
        self.output_tree = FileTreeWidget(self, "output")
        self.output_tree.setHeaderLabel("输出文件夹结构")
        
        tree_layout = QtWidgets.QHBoxLayout()
        tree_layout.addWidget(self.input_tree)
        tree_layout.addWidget(self.output_tree)
        
        # Start conversion button
        start_button = QtWidgets.QPushButton("开始转换")
        start_button.setStyleSheet("""
            background-color: yellow;  /* 设置按钮背景颜色为亮黄色 */
            border: 2px solid lightyellow;  /* 添加淡黄色高亮边框 */
            border-radius: 5px;  /* 可选：添加圆角 */
        """)
        start_button.clicked.connect(self.start_conversion)

        
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addLayout(checkbox_layout)
        layout.addLayout(tree_layout)
        layout.addWidget(start_button)
        
        self.home_tab.setLayout(layout)

    def select_input(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if path:
            self.input_path.setText(path)
            self.input_tree.populate_tree(pathlib.Path(path))

    def select_output(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if path:
            self.output_path.setText(path)
            self.output_tree.populate_tree(pathlib.Path(path))

    def rename_output_folder_checked(self, state):
        if state == QtCore.Qt.Checked and self.names_obj:
            output_path = pathlib.Path(self.output_path.text())
            if output_path.exists():
                new_output_path = output_path.parent / self.names_obj.new_folder
                output_path.rename(new_output_path)
                self.output_path.setText(str(new_output_path))

    def start_conversion(self):
        input_path = pathlib.Path(self.input_path.text())
        output_path = pathlib.Path(self.output_path.text())
        
        for bmson_file in input_path.glob("*.bmson"):
            self.names_obj = process_file(bmson_file, output_path, self.include_audio.isChecked(), self.include_images.isChecked())
            if self.rename_output_folder.isChecked() and self.names_obj:
                new_output_path = output_path.parent / self.names_obj.new_folder
                output_path.rename(new_output_path)
                self.output_path.setText(str(new_output_path))

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
                    self.parent().input_path.setText(str(path))
                elif self.tree_type == "output":
                    self.parent().output_path.setText(str(path))