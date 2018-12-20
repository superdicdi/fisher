import requests

__author__ = "TuDi"
__date__ = "2018/12/17 上午11:47"


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url=url)
        if int(r.status_code) == 200:
            return r.json() if return_json else r.text
        return {} if return_json else ""
