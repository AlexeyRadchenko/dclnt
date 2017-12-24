from django.conf.urls import url
from .views import ManagementLogin, ManagementOperatorRKC


urlpatterns = [
    url(r'^login/$', ManagementLogin.as_view(), name='management_login'),
    url(r'^(?P<username>\w+)/$', ManagementOperatorRKC.as_view(), name='operator_panel'),
]
