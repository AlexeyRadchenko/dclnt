from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout


class ManagementLogin(View):
    template = 'management/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'ok': '/management/{}/'.format(user)})
        else:
            return JsonResponse({'error': 'неверный логин или пароль'})


class ManagementOperatorRKC(View):
    template = 'management/operator.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template)
        else:
            return redirect('management_login')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('management_login')
