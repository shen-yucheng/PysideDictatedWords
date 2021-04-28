import pypinyin
import re
import zipfile
import io
import os
import random


class Text:
    text_html = None
    answer_html = None

    def __init__(self, words_text: str, title="看音写词"):
        """
        words_split_by_enter_or_space
        """

        def pinyin(word):
            return " ".join(
                (each_pinyin[0] for each_pinyin in pypinyin.pinyin(word))
            )

        self.title = title
        self.raw_text = words_text

        # 去除换行符
        words_text = re.sub(
            r"\\.",
            " ",
            repr(words_text)[1:-1]
        )

        # 去除多余空格
        words_text = re.sub(
            r"\s+",
            " ",
            words_text
        )

        words = words_text.split(" ")
        random.shuffle(words)

        self.words_html = "".join([
            rf'<div class="question"><p class="pinyin">{pinyin(each_word)}</p><p class="kuohao">（</p><pre class="kuohao answer">{each_word :^{round(len(each_word) * 2.5)}}</pre><p class="kuohao">）</p></div>'
            for each_word in words])

    def get_text_html(self):
        if not self.text_html:
            style = "<style>h1{margin:1em}.question{display:inline-block;font-size:20px;margin:0.5em}.pinyin{text-align:center;margin:0 0 0.5em}.kuohao{margin:0;display:inline-block}.answer{color:transparent}</style>"
            self.text_html = fr'<!doctype html><html lang="zh-cn"><head><meta charset="UTF-8"><meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"name="viewport"><meta content="ie=edge"http-equiv="X-UA-Compatible">{style}<title>{self.title}</title></head><body><h1>{self.title}</h1>{self.words_html}</body></html>'

        return self.text_html

    def get_answer_html(self):
        if not self.answer_html:
            style = "<style>h1{margin:1em}.question{display:inline-block;font-size:20px;margin:0.5em}.pinyin{text-align:center;margin:0 0 0.5em}.kuohao{margin:0;display:inline-block}</style>"
            self.answer_html = fr'<!doctype html><html lang="zh-cn"><head><meta charset="UTF-8"><meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"name="viewport"><meta content="ie=edge"http-equiv="X-UA-Compatible">{style}<title>{self.title} 答案</title></head><body><h1>{self.title}</h1>{self.words_html}</body></html>'

        return self.answer_html

    def get_zip(self) -> io.BytesIO:
        file = io.BytesIO()
        zip_file = zipfile.ZipFile(
            file,
            "w"
        )

        zip_file.writestr(
            f"{self.title} 答案.html",
            self.get_answer_html()
        )
        zip_file.writestr(
            f"{self.title}.html",
            self.get_text_html()
        )
        zip_file.writestr(
            f"{self.title} 源词.txt",
            self.raw_text
        )

        zip_file.close()
        file.seek(0)

        return file

    def write_zip(self, file_name: str):
        open(file_name, "wb").write(
            self.get_zip().getvalue()
        )

    def write_folder(self, folder_name: str):
        os.makedirs(folder_name)

        open(fr"{folder_name}/{self.title} 答案", "w").write(
            self.get_answer_html()
        )
        open(fr"{folder_name}/{self.title}.html", "w").write(
            self.get_text_html()
        )
        open(fr"{folder_name}/{self.title} 原词.txt", "w").write(
            self.raw_text
        )
