from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired

__author__ = "TuDi"
__date__ = "2018/12/17 下午8:36"


class SearchForm(Form):
    q = StringField(
        validators=[
            Length(min=1, max=30),
            DataRequired("搜索内容不能为空")
        ]
    )

    page = IntegerField(
        validators=[
            NumberRange(min=1, max=3),
        ],
        default=1
    )

