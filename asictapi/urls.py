"""
URLs for mobile WEBAPI
"""
from django.conf import settings
from django.conf.urls import patterns, url


# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^heartbeat', 'asictapi.views.heartbeat', name='asictapi_heartbeat'),
    url(r'^get_certs/(?P<date_certs>[^/]+)', 'asictapi.views.certs_download', name='asictapi_certs_download'),
)
