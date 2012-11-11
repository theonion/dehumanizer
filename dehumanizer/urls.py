from django.conf.urls import patterns, url

urlpatterns = patterns('dehumanizer.core.views',
    url(r'^$', 'home'),
    url(r'^image(?P<extension>\.json)?$', 'process'),
)
