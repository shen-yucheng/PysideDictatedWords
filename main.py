import sys

import dictated_words as text


@PySide2.QtCore.Slot()
def start():
    try:
        title = title_entry.text()
        text.Text(
            words_text=content_entry.toPlainText(),
            title=title
        ).write_zip(
            PySide2.QtWidgets.QFileDialog.getSaveFileName(
                main_widget,
                "保存看音写词",
                title,
                r"All Files (*);;Zip Files (*.zip)"
            )[0]
        )

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



