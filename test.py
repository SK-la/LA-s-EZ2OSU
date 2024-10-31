import json
import pathlib
from Dispatch_data import dispatch
#from    ui.MainWindow import ConversionSettings

            # 获取复选框和下拉框的值
settings = ()

def test_process_data(file_path):
    file_path = pathlib.Path(file_path)
    if not file_path.exists() or not file_path.is_file():
        print(f"File does not exist: {file_path}")
        return

    try:
        with file_path.open('r', encoding='utf-8') as file:
            data = json.load(file)
        print("数据可读")



        try:
            osu_content = dispatch(data, settings)
            print("调度逻辑无问题\n")
        except Exception as e:
            print(f"Error in process_data: {e}")
            return

        # Output all query values
        
        #print(osu_content)


    except Exception as e:
        print(f"调度出错: {e}")

# Example call
test_process_data(r"E:\BASE CODE\GitHub\LAs-EZ2OSU\test\testdata.bmson")
