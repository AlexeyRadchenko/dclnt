from django.conf.urls import url
from .views import test, update_progress_bar
urlpatterns = [
    url(r'^$', test),
    url(r'^progressbar_update/$', update_progress_bar),
]