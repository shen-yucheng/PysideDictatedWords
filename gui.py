import sys
import PySide2.QtGui
import PySide2.QtCore
import PySide2.QtWidgets
import sys
import dictated_words
import zipfile

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
        self.setWindowTitle(self.title)
        self.setWindowIcon(PySide2.QtGui.QIcon("icon.svg"))
        desktop_widget = PySide2.QtWidgets.QDesktopWidget()
        self.resize(desktop_widget.width() * 0.7, desktop_widget.height() * 0.7)
        self.setStyleSheet(open("main.qss").read())
        self.setCentralWidget(self.content_entry)

        # 菜单设置
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("文件")
        file_menu.addAction("重命名").triggered.connect(self.rename)
        file_menu.addAction("保存").triggered.connect(self.save)
        file_menu.addAction("另存为").triggered.connect(self.save_as)

        menu_bar.addMenu("编辑")

        menu_bar.addMenu("帮助")

        self.count()

        # 打开文件
        if len(sys.argv) > 1:
            self.load_file(sys.argv[1])

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

    def write(self, file_name):
        # 看音写词
        dictated_words.Text(
            words_text=self.content_entry.toPlainText(),
            title=self.title
        ).write_zip(file_name)

        # 完成提示
        messageBox = PySide2.QtWidgets.QMessageBox()
        messageBox.information(
            main_window,
            "生成看音写词",
            "完成",
        )

    @PySide2.QtCore.Slot()
    def rename(self):
        _input = PySide2.QtWidgets.QInputDialog.getText(self, "重命名看音写词", "请输入新名称")
        if _input[1]:
            self.title = _input[0]

        self.setWindowTitle(self.title)

    @PySide2.QtCore.Slot()
    def save(self):
        if not self.file_path:
            self.file_path = PySide2.QtWidgets.QFileDialog.getSaveFileName(
                self,
                "保存看音写词",
                self.title,
                r"All Files (*);;Zip Files (*.zip)"
            )[0]

        self.write(file_name=self.file_path)

    @PySide2.QtCore.Slot()
    def save_as(self):
        file_path = PySide2.QtWidgets.QFileDialog.getSaveFileName(
            self,
            "另存看音写词",
            self.title,
            r"All Files (*);;Zip Files (*.zip)"
        )[0]

        self.write(file_path)

    def load_file(self, file_path):
        zip_ = zipfile.ZipFile(file_path, 'r')
        for each_name in zip_.namelist():
            if "原词" in each_name:
                break

        self.file_path = file_path
        self.title = each_name
        self.setWindowTitle(each_name)
        self.content_entry.setPlainText(
            zip_.read(each_name).decode('utf-8')
        )


main_window = Editor()
main_window.show()
app.exec_()
