from django.conf.urls import url
from .views import AccountsLoginView, AccountsView, AccountsLogoutView


urlpatterns = [
    url(r'^login/$', AccountsLoginView.as_view(), name='accounts_login'),
    url(r'^logout/$', AccountsLogoutView.as_view(), name='accounts_logout'),
    url(r'^(?P<username>\w+)/$', AccountsView.as_view(), name='accounts_panel'),

]
