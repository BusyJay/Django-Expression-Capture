# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from utils.forms import ExpressionCaptureForm

__author__ = 'jay'


class TestLoginForm(ExpressionCaptureForm):
    email = forms.EmailField(label=_('username'), required=True)
    password = forms.CharField(label=_('password'), required=True)
