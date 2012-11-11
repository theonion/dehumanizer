from django.conf.urls import patterns, url

urlpatterns = patterns('asciizer.core.views',
    url(r'^$', 'home'),
    url(r'^image(?P<extension>\.json)?$', 'process'),
)
