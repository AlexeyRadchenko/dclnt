from django.conf.urls import url
from catalog.views import CatalogView, ProductView

urlpatterns = [
    url(r'^$', CatalogView.as_view(), name='catalog'),
    url(r'^product/(?P<product_id>\d+)$', ProductView.as_view(), name='product'),
]