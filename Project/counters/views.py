from django.views.generic import TemplateView


class StartDevPage(TemplateView):
    template_name = 'counters/test.html'

