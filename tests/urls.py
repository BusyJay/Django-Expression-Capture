from django.conf.urls.defaults import patterns, url

__author__ = 'jay'


urlpatterns = patterns('tests.views',
                       url(r'', 'index', name='index_page'),
                       )

