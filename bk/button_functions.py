# # ui/button.py
# from PyQt5 import QtWidgets
# import pathlib

# def select_input(main_window):
#     path = QtWidgets.QFileDialog.getExistingDirectory(main_window, "选择输入文件夹")
#     if path:
#         main_window.input_path.setText(path)
#         main_window.home_tab.input_tree.populate_tree(pathlib.Path(path))

# def select_output(main_window):
#     path = QtWidgets.QFileDialog.getExistingDirectory(main_window, "选择输出文件夹")
#     if path:
#         main_window.output_path.setText(path)
#         main_window.home_tab.output_tree.populate_tree(pathlib.Path(path))

# def start_conversion(main_window):
#     input_path = pathlib.Path(main_window.input_path.text())
#     output_path = pathlib.Path(main_window.output_path.text())
    
#     # 获取复选框和下拉框的值
#     settings = ConversionSettings(
#         include_audio=main_window.include_audio.isChecked(),
#         include_images=main_window.include_images.isChecked(),
#         remove_empty_columns=main_window.remove_empty_columns.isChecked(),
#         lock_cs_set=main_window.lock_cs_set.isChecked(),
#         lock_cs_num=main_window.lock_cs_num_combobox.currentText()
#     )
    
#     for bmson_file in input_path.glob("**/*.bmson"):
#         # 在输出路径中创建对应的子目录
#         relative_path = bmson_file.relative_to(input_path)
#         target_dir = output_path / relative_path.parent
#         target_dir.mkdir(parents=True, exist_ok=True)
        
#         # 处理文件并保存到对应的子目录
#         main_window.names_obj = process_file(bmson_file, target_dir, settings)

#     # 更新文件树
#     main_window.home_tab.input_tree.populate_tree(input_path)
#     main_window.home_tab.output_tree.populate_tree(output_path)
