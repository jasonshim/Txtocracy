from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^sms/status/$', 'txtmessages.views.sms_status_update', name='sms_status_update')
)
