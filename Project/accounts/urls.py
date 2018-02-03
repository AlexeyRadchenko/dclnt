from django.conf.urls import url
from .views import AccountsLoginView, AccountsView


urlpatterns = [
    url(r'^login/$', AccountsLoginView.as_view(), name='accounts_login'),
    url(r'^(?P<username>\w+)/$', AccountsView.as_view(), name='account_panel'),
]