# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

__author__ = 'jay'


class ExpressionCapture(forms.TextInput):

    def __init__(self, attrs=None):
        super(ExpressionCapture, self).__init__(attrs)
        self.image_width, self.image_height, self.image_url = 0, 0, None

    def set_image_width(self, w):
        self.image_width = w

    def set_image_height(self, h):
        self.image_height = h

    def set_image_url(self, u):
        self.image_url = u

    def render(self, name, value, attrs=None):
        render_text = super(ExpressionCapture, self).render(name, value, attrs)
        w_attr, h_attr = '', ''
        if self.image_width:
            w_attr = 'width="%s"' % self.image_width
        if self.image_height:
            h_attr = 'height="%s"' % self.image_height
        refresh_url = self.image_url
        if '?' in self.image_url:
            refresh_url += '&time='
        else:
            refresh_url += '?'
        img = u' <img style="cursor: pointer" %s %s onclick="this.src=\'%s\'+new Date().getTime()" src="%s">'
        return render_text + (img % (w_attr, h_attr, refresh_url, refresh_url))


class ExpressionCaptureForm(forms.Form):
    expression_capture = forms.CharField(label=_('Answer'), required=True, widget=ExpressionCapture,
                                         error_messages={'required': _("Capture field can't be empty")})

    def __init__(self, request, captureId='capture', *args, **kwargs):
        self._validate_code = None
        if request.POST:
            super(ExpressionCaptureForm, self).__init__(request.POST, *args, **kwargs)
            self.host = request.get_host()
            self._validate_code = request.session.get(captureId, None)
        else:
            super(ExpressionCaptureForm, self).__init__(*args, **kwargs)
        request.session[captureId] = False
        self.fields['expression_capture'].widget.set_image_url('/utils/capture')
        self.fields.keyOrder.append(self.fields.keyOrder.pop(0))  # because expression_capture should always be the first

    def clean_expression_capture(self):
        expression_capture = self.cleaned_data['expression_capture']
        answer_code = self._validate_code
        print(answer_code, expression_capture)
        if expression_capture == answer_code:
            return expression_capture
        if answer_code is None:
            raise forms.ValidationError(_('Capture is out of date!'))
        raise forms.ValidationError(_('Answer is wrong!'))

    def is_capture_correct(self):
        """
        Valid only when called from clean()
        """
        return self.cleaned_data.get('expression_capture', None) is not None

