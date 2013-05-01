from django.conf.urls.defaults import patterns, url

__author__ = 'jay'

urlpatterns = patterns('utils.views',
                       url(r'^capture', 'generate_capture', name='capture_generator'),
                       )
