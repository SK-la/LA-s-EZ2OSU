import asyncio
import sys

from PyQt6 import QtWidgets
from qasync import QEventLoop

from ui.MainWindow import MainWindow  # 确保路径正确

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    with loop:
        loop.run_forever()
