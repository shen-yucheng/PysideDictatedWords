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
            "完成",
        )
    except Exception as error:
        messageBox = PySide2.QtWidgets.QMessageBox()
        messageBox.critical(
            main_window,
            "生成看音写词",
            str(error),
        )


PySide2.QtCore.QCoreApplication.setAttribute(PySide2.QtCore.Qt.AA_EnableHighDpiScaling)
app = PySide2.QtWidgets.QApplication(sys.argv)

# 单个组件
title_entry = PySide2.QtWidgets.QLineEdit()
title_entry.setPlaceholderText("标题")
title_entry_layout = PySide2.QtWidgets.QHBoxLayout()
title_entry_layout.addWidget(title_entry)
title_entry_layout.addStretch()

content_entry = PySide2.QtWidgets.QTextEdit()
content_entry.setPlaceholderText("看音写词词语，用空格分割")

start_button = PySide2.QtWidgets.QPushButton("启动")
start_button.setObjectName("start_button")
start_button.clicked.connect(start)
start_button_layout = PySide2.QtWidgets.QHBoxLayout()
start_button_layout.addStretch()
start_button_layout.addWidget(start_button)

# 总体窗口布局
layout = PySide2.QtWidgets.QVBoxLayout()
layout.addLayout(title_entry_layout)
layout.addWidget(content_entry)
layout.addLayout(start_button_layout)

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
