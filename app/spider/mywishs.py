from app.libs.http_tool import HTTP
from app.spider.yushu_book import YuShuBook

__author__ = "TuDi"
__date__ = "2018/12/17 下午1:13"


class MyWishes:

    def __init__(self):
        self.wishs = []

    def __fill_single(self, data, count):
        if data:
            self.wishs.append({"wishes_count": count, "book": YuShuBook.cut_book_data(data)})

    def search_by_isbns(self, wish_isbns, gift_count):
        # 将我想赠送但无人想要的书籍添加进 gifts 中并将 count 赋值为 0
        for isbn in wish_isbns:
            result = HTTP.get(YuShuBook.isbn_url.format(isbn))
            count = 0
            for gift in gift_count:
                if isbn in gift.values():
                    count = gift["count"]
                    break
            self.__fill_single(result, count)
        return sorted(self.wishs, key=lambda x: x["wishes_count"], reverse=True)

