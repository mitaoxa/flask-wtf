from wtforms.compat import with_metaclass
from wtforms.form import FormMeta

from flask_wtf import CsrfProtect, FlaskForm, Form
from flask_wtf._compat import FlaskWTFDeprecationWarning


def test_deprecated_form(req_ctx, recwarn):
    class F(Form):
        pass

    F()
    w = recwarn.pop(FlaskWTFDeprecationWarning)
    assert 'FlaskForm' in str(w.message)


def test_custom_meta_with_deprecated_form(req_ctx, recwarn):
    class FMeta(FormMeta):
        pass

    class F(with_metaclass(FMeta, Form)):
        pass

    F()
    recwarn.pop(FlaskWTFDeprecationWarning)


def test_deprecated_html5(recwarn):
    __import__('flask_wtf.html5')
    w = recwarn.pop(FlaskWTFDeprecationWarning)
    assert 'wtforms.fields.html5' in str(w.message)


def test_deprecated_csrf_enabled_param(req_ctx, recwarn):
    class F(FlaskForm):
        pass

    F(csrf_enabled=False)
    w = recwarn.pop(FlaskWTFDeprecationWarning)
    assert 'meta.csrf' in str(w.message)


def test_deprecated_csrfprotect(recwarn):
    CsrfProtect()
    w = recwarn.pop(FlaskWTFDeprecationWarning)
    assert 'CSRFProtect' in str(w.message)
