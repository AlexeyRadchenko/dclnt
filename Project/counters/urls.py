from django.conf.urls import url
from .views import StartDevPage

urlpatterns = [
    url(r'^$', StartDevPage.as_view()),
]
