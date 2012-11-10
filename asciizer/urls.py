from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('asciizer.core.views',
    url(r'^$', 'home'),
    url(r'^process(?P<format>\.json)?$', 'process'),
    url(r'^(?P<pk>\d+)$', 'image'),
    # url(r'^asciizer/', include('asciizer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
