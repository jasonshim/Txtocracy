from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url("^$", "pledge.views.home", name="home"),
    url("^(\d{4})/(.*)/info/$", "pledge.views.election", name="election"),
    url("^(\d{4})/(.*)/$", "pledge.views.pledge", name="pledge"),   
)
