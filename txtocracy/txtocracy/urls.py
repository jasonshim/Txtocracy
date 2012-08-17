from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('pledge.urls')),
    url(r'^txtadmin/', include(admin.site.urls)),
)
