import pytest
from werkzeug.datastructures import FileStorage
from wtforms import FileField

from flask_wtf import FlaskForm
from flask_wtf._compat import FlaskWTFDeprecationWarning
from flask_wtf.file import FileAllowed, FileField as OldFileField, FileRequired


@pytest.fixture
def form(req_ctx):
    class UploadForm(FlaskForm):
        class Meta:
            csrf = False

        file = FileField()

    return UploadForm


def test_file_required(form):
    form.file.kwargs['validators'] = [FileRequired()]

    f = form()
    assert not f.validate()
    assert f.file.errors[0] == 'This field is required.'

    f = form(file='not a file')
    assert not f.validate()
    assert f.file.errors[0] == 'This field is required.'

    f = form(file=FileStorage())
    assert f.validate()


def test_file_allowed(form):
    form.file.kwargs['validators'] = [FileAllowed(('txt',))]

    f = form()
    assert f.validate()

    f = form(file=FileStorage(filename='test.txt'))
    assert f.validate()

    f = form(file=FileStorage(filename='test.png'))
    assert not f.validate()
    assert f.file.errors[0] == 'File does not have an approved extension: txt'


def test_file_allowed_uploadset(app, form):
    pytest.importorskip('flask_uploads')
    from flask_uploads import UploadSet, configure_uploads

    app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
    txt = UploadSet('txt', extensions=('txt',))
    configure_uploads(app, (txt,))
    form.file.kwargs['validators'] = [FileAllowed(txt)]

    f = form()
    assert f.validate()

    f = form(file=FileStorage(filename='test.txt'))
    assert f.validate()

    f = form(file=FileStorage(filename='test.png'))
    assert not f.validate()
    assert f.file.errors[0] == 'File does not have an approved extension.'


def test_deprecated_filefield(recwarn, req_ctx):
    class F(FlaskForm):
        f = OldFileField()

    w = recwarn.pop(FlaskWTFDeprecationWarning)
    assert 'wtforms.FileField' in str(w.message)

    assert not F().f.has_file()
    assert F(f=FileStorage()).f.has_file()
