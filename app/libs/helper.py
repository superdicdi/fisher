__author__ = "TuDi"
__date__ = "2018/12/17 上午11:29"


def is_isbn_or_key(word):
    """
    根据 word 判断用户是 sbin 查询还是关键字查询
    """
    isbn_or_key = "key"
    # isbn 由13个0~9的数字组成
    # isbn 含有10个0~9的数字组成，可能额外包括一些"-"
    if len(word) == 13 and word.isdigit():
        isbn_or_key = "isbn"
    short_word = word.replace("-", "")
    if len(short_word) == 10 and "-" in word and short_word.isdigit():
        isbn_or_key = "isbn"
    return isbn_or_key
