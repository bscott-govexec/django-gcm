from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^device/$', 'gcm.views.device', name='gcm-device'),
)
