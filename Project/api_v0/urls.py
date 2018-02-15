from django.conf.urls import url, include
from rest_framework import routers

from .views import ListUsers, FileUploadView, UpdateProgressBarView, GetAccountFormAndData, SaveAccountNewData,\
    FileDownloadView

router = routers.SimpleRouter()
router.register(r'users', ListUsers, base_name='users')

urlpatterns = [
    url(r'^upload/$', FileUploadView.as_view()),
    url(r'^download/$', FileDownloadView.as_view()),
    url(r'^progressbar_update/$', UpdateProgressBarView.as_view()),
    url(r'^get_account_data/$', GetAccountFormAndData.as_view()),
    url(r'^save_account_new_data/$', SaveAccountNewData.as_view()),
    url(r'^', include(router.urls))
]
