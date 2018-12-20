__author__ = "TuDi"
__date__ = "2018/12/20 上午11:48"


class BookViewModels:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            "books": [],
            "keyword": keyword,
            "total": 0
        }
        if data:
            returned["total"] = 1
            returned["books"] = [cls._cut_book_data(data)]
        return returned

    @classmethod
    def package_collect(cls, data, keyword):
        returned = {
            "books": [],
            "keyword": keyword,
            "total": data["total"]
        }
        if data["books"]:
            returned["books"] = [cls._cut_book_data(book) for book in data["books"]]
        return returned

    @classmethod
    def _cut_book_data(cls, data):
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "pages": data["pages"] or "暂无",
            "author": "、".join(data["author"]),
            "price": data["price"],
            "summary": data["summary"] or "暂无",
            "image": data["image"]
        }
        return book
