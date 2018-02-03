from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class AccountsLoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'ok': '/accounts/{}/'.format(user)})
        else:
            return JsonResponse({'error': 'неверный логин или пароль'})


class AccountsView(TemplateView):
    template_name = 'profile.html'

    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context"""