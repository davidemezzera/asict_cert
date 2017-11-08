"""
URLs for mobile WEBAPI
"""
from django.conf import settings
from django.conf.urls import patterns, url
from .views import CreateView


# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^heartbeat', CreateView.as_view(), name = 'asictapi_heartbeat'),
    #url(r'^get_certs/last', 'asictapi.views.certs_download_yesterday', name = 'certs_download_yesterday'),
    #url(r'^get_certs/(?P<start_date>[^/]+)/(?P<end_date>[^/]+)', 'asictapi.views.certs_download', name = 'asictapi_certs_download'),
)
