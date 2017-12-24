from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ListUsers

router = routers.SimpleRouter()
router.register(r'users', ListUsers, base_name='users')

urlpatterns = router.urls
print(router.urls)
"""
urlpatterns = format_suffix_patterns([
    #url(r'^$', api_root),
    url(r'^users/$', ListUsers, name='user-list'),
])"""