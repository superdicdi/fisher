from app.libs.http_tool import HTTP
from app.spider.yushu_book import YuShuBook

__author__ = "TuDi"
__date__ = "2018/12/17 下午1:13"


class MyGifts:

    def __init__(self):
        self.gifts = []

    def __fill_single(self, data, count, gift_id):
        if data:
            self.gifts.append({"wishes_count": count, "book": YuShuBook.cut_book_data(data), "id": gift_id})

    def search_by_isbns(self, gifts, wish_count):
        # 将我想赠送但无人想要的书籍添加进 gifts 中并将 count 赋值为 0
        for gift in gifts:
            result = HTTP.get(YuShuBook.isbn_url.format(gift.isbn))
            count = 0
            for wish in wish_count:
                if gift.isbn in wish.values():
                    count = wish["count"]
                    break
            self.__fill_single(result, count, gift.id)
        return sorted(self.gifts, key=lambda x: x["wishes_count"], reverse=True)

