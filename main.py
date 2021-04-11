import sys
import PySide2.QtGui
import PySide2.QtCore
import PySide2.QtWidgets
import dictated_words as text


@PySide2.QtCore.Slot()
def start():
    try:
        text.Text(
            words_text=content_entry.toPlainText(),
            raw_html=open("print.html").read(),
            title=(title := title_entry.text())
        ).write_folder(fr"..\{title}")

        messageBox = PySide2.QtWidgets.QMessageBox()
        messageBox.information(
            main_window,
            "生成看音写词",
            "完成（关闭程序时才能写入文件夹）",
        )
        messageBox.show()
    except Exception as error:
        messageBox = PySide2.QtWidgets.QMessageBox()
        messageBox.critical(
            main_window,
            "生成看音写词",
            str(error),
        )
        messageBox.show()


PySide2.QtCore.QCoreApplication.setAttribute(PySide2.QtCore.Qt.AA_EnableHighDpiScaling)
app = PySide2.QtWidgets.QApplication(sys.argv)

# 单个组件
title_label = PySide2.QtWidgets.QLabel("标题：")
title_entry = PySide2.QtWidgets.QLineEdit()
title_entry_layout = PySide2.QtWidgets.QHBoxLayout()
title_entry_layout.addWidget(title_entry)
title_entry_layout.addStretch()
title_entry_frame = PySide2.QtWidgets.QWidget()
title_entry_frame.setObjectName("title_entry_frame")
title_entry_frame.setLayout(title_entry_layout)
title_frame_layout = PySide2.QtWidgets.QVBoxLayout()
title_frame_layout.addWidget(title_label)
title_frame_layout.addWidget(title_entry_frame)
title_frame = PySide2.QtWidgets.QWidget()
title_frame.setLayout(title_frame_layout)

content_label = PySide2.QtWidgets.QLabel("词语：")
content_entry = PySide2.QtWidgets.QTextEdit()
content_entry.setPlaceholderText("用空格分割")
content_frame_layout = PySide2.QtWidgets.QVBoxLayout()
content_frame_layout.addWidget(content_label)
content_frame_layout.addWidget(content_entry)
content_frame = PySide2.QtWidgets.QWidget()
content_frame.setLayout(content_frame_layout)

start_button = PySide2.QtWidgets.QPushButton("启动")
start_button.clicked.connect(start)
button_frame_layout = PySide2.QtWidgets.QHBoxLayout()
button_frame_layout.addStretch()
button_frame_layout.addWidget(start_button)
button_frame = PySide2.QtWidgets.QWidget()
button_frame.setLayout(button_frame_layout)

# 总体窗口布局
layout = PySide2.QtWidgets.QVBoxLayout()

layout.addWidget(title_frame)
layout.addWidget(content_frame)
layout.addWidget(button_frame)

main_widget = PySide2.QtWidgets.QWidget()
main_widget.setLayout(layout)

main_window = PySide2.QtWidgets.QMainWindow()
main_window.setWindowTitle("生成看音写词")
main_window.setWindowIcon(
    PySide2.QtGui.QIcon("icon.svg")
)
desktop_widget = PySide2.QtWidgets.QDesktopWidget()
main_window.resize(
    desktop_widget.width() * 0.7,
    desktop_widget.height() * 0.7
)
main_window.setCentralWidget(main_widget)

main_window.setStyleSheet(
    open("main.qss").read()
)

main_window.show()
app.exec_()
