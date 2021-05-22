import PySide2.QtGui
import PySide2.QtCore
import PySide2.QtWidgets
import sys
import dictated_words

app = PySide2.QtWidgets.QApplication(sys.argv)


class Editor(PySide2.QtWidgets.QMainWindow):
    file_path = None
    title = "新看音写词"

    def __init__(self):
        super(Editor, self).__init__()

        # 输入框组件
        self.content_entry = PySide2.QtWidgets.QPlainTextEdit()
        self.content_entry.setObjectName("main_entry")
        self.content_entry.setPlaceholderText("看音写词词语，用空格分割")
        self.content_entry.setVerticalScrollBarPolicy(PySide2.QtCore.Qt.ScrollBarAlwaysOn)
        self.content_entry.textChanged.connect(self.count)

        # 状态栏设置
        self.count_label = PySide2.QtWidgets.QLabel()
        self.count_label.setObjectName("count_label")
        self.statusBar().addWidget(self.count_label)

        # 窗口设置
        self.setWindowTitle("生成看音写词")
        self.setWindowIcon(PySide2.QtGui.QIcon("icon.svg"))
        desktop_widget = PySide2.QtWidgets.QDesktopWidget()
        self.resize(desktop_widget.width() * 0.7, desktop_widget.height() * 0.7)
        self.setStyleSheet(open("main.qss").read())
        self.setCentralWidget(self.content_entry)

        # 菜单设置
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("文件")
        file_menu.addAction("保存").triggered.connect(self.save)

        self.menuBar().addMenu("编辑")

        self.menuBar().addMenu("帮助")

        self.count()

    @PySide2.QtCore.Slot()
    def count(self) -> tuple:
        """
        统计输入信息的字数、词数、行数并显示
        返回输入信息的字数、词数、行数
        """

        # 获取词列表
        input_text: str = self.content_entry.toPlainText()
        words_list = dictated_words.format_words_text(input_text).split(" ")
        if "" in words_list:
            words_list.remove('')

        # 统计字，词，行数
        character_length = len(
            ''.join(words_list)
        )
        words_length = len(words_list)
        lines_length = input_text.count("\n")

        # 显示统计信息
        # 如果字符数为零显示“准备就绪”，如果字符数不为零显示统计数据
        count_message = f"{character_length}个字，{words_length}个词，{lines_length}行" if character_length else "准备就绪"
        self.count_label.setText(count_message)

        return character_length, words_length, lines_length

    @PySide2.QtCore.Slot()
    def save(self):
        dictated_words.Text(
            words_text=self.content_entry.toPlainText(),
            title=self.title
        ).write_zip(
            PySide2.QtWidgets.QFileDialog.getSaveFileName(
                self,
                "保存看音写词",
                self.title,
                r"All Files (*);;Zip Files (*.zip)"
            )[0]
        )

        # 完成提示
        messageBox = PySide2.QtWidgets.QMessageBox()
        messageBox.information(
            main_window,
            "生成看音写词",
            "完成",
        )


main_window = Editor()
main_window.show()
app.exec_()
