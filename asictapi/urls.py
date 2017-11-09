"""
URLs for mobile WEBAPI
"""
from django.conf import settings
from django.conf.urls import patterns, url
#from .views import AunicaCertView

'''
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^heartbeat', AunicaCertView.as_view(), name = 'asictapi_heartbeat'),
    #url(r'^get_certs/last', 'asictapi.views.certs_download_yesterday', name = 'certs_download_yesterday'),
    #url(r'^get_certs/(?P<start_date>[^/]+)/(?P<end_date>[^/]+)', 'asictapi.views.certs_download', name = 'asictapi_certs_download'),
)'''

from .views import MyRESTView

urlpatterns = patterns('',
    # this URL passes resource_id in **kw to MyRESTView
    url(r'^heartbeat', MyRESTView.as_view(), name='my_rest_view'),
)