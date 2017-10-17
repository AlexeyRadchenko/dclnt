from django.views.generic import ListView, DetailView
from catalog.models import Product


class CatalogView(ListView):
    model = Product
    template_name = 'product_list.html'


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    pk_url_kwarg = 'product_id'


