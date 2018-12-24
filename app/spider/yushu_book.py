from flask import current_app

from app.libs.http_tool import HTTP

__author__ = "TuDi"
__date__ = "2018/12/17 下午1:13"


class YuShuBook:
    isbn_url = "http://t.yushu.im/v2/book/isbn/{0}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={0}&count={1}&start={2}"

    def __init__(self):
        self.books = []
        self.keyword = ""
        self.total = 0

    def __fill_single(self, data):

        if data:
            self.total = 1
            self.books.append(self._cut_book_data(data))

    def __fill__collection(self, data):
        if data["books"]:
            self.total = data["total"]
            self.books = [self._cut_book_data(book) for book in data["books"]]

    @staticmethod
    def _cut_book_data(data):
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "pages": data["pages"] or "暂无",
            "author": "、".join(data["author"]),
            "price": data["price"],
            "summary": data["summary"] or "暂无",
            "image": data["image"],
            "isbn": data["isbn"],
            "pubdate": data["pubdate"],
            "binding": data["binding"] or "暂无信息",
            "intro": " / ".join(
                filter(lambda x: True if x else False, ["、".join(data["author"]), data["publisher"], data["price"]]))
        }
        return book

    def search_by_isbn(self, keyword):
        result = HTTP.get(self.isbn_url.format(keyword))
        self.__fill_single(result)
        self.keyword = keyword

    def search_by_keyword(self, keyword, page=1):
        result = HTTP.get(self.keyword_url.format(keyword, current_app.config["PER_PAGE"], self.calculate_page(page)))
        self.__fill__collection(result)
        self.keyword = keyword

    @staticmethod
    def calculate_page(page):
        return (page - 1) * current_app.config["PER_PAGE"]

    @property
    def first(self):
        return self.books[0] if self.books else {}