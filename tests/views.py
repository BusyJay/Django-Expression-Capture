# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from tests.forms import TestLoginForm


def index(request):
    extra_context = {}
    if request.method == 'POST':
        form = TestLoginForm(request)
        if form.is_valid():
            extra_context['msg'] = 'Valid！'
    else:
        form = TestLoginForm(request)

    extra_context['form'] = form
    return render_to_response('index.html', extra_context, context_instance=RequestContext(request))

