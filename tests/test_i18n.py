# coding=utf8
from flask import request
from flask_babel import Babel
from wtforms import StringField
from wtforms.validators import DataRequired

from flask_wtf import FlaskForm


class NameForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField(validators=[DataRequired()])


def test_i18n_disabled(app, client):
    @app.route('/', methods=['POST'])
    def index():
        form = NameForm()
        form.validate()
        assert form.name.errors[0] == 'This field is required.'

    client.post(
        '/', headers={'Accept-Language': 'zh-CN,zh;q=0.8'}
    )


def test_i18n_enabled(app, client):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(['en', 'zh'], 'en')

    @app.route('/', methods=['POST'])
    def index():
        form = NameForm()
        form.validate()
        assert form.name.errors[0] == u'该字段是必填字段。'

    client.post(
        '/', headers={'Accept-Language': 'zh-CN,zh;q=0.8'},
    )
