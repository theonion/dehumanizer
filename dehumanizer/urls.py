from django.conf.urls import patterns, url

from django.views.generic import TemplateView

urlpatterns = patterns('dehumanizer.core.views',
    url(r'^$', 'home'),
    url(r'^image(?P<extension>\.json)?$', 'process'),
    url(r'^embed$', 'embed'),
    url(r'^channel\.html$', TemplateView.as_view(template_name="channel.html"))
)
