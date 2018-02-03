from django.conf.urls import url, include
from rest_framework import routers

from .views import ListUsers, FileUploadView, UpdateProgressBarView

router = routers.SimpleRouter()
router.register(r'users', ListUsers, base_name='users')

urlpatterns = [
    url(r'^upload/$', FileUploadView.as_view()),
    url(r'^progressbar_update/$', UpdateProgressBarView.as_view()),
    url(r'^', include(router.urls))
]
