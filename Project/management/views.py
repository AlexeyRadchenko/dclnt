from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin

from api_v0.forms import FileFieldForm
from counters.models import Accounts


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


class ManagementOperatorRKC(UserPassesTestMixin, View):
    template = 'management/operator.html'
    context = None
    login_url = '/management/login/'

    def test_func(self):
        return self.check_group()

    @staticmethod
    def str_to_num(text):
        try:
            return int(text)
        except ValueError:
            return 0

    @staticmethod
    def get_houses_list():
        return Accounts.objects.order_by('street').values('street', 'house_number').distinct()

    def get_apartments_of_house(self, houses):
        apartments = []
        for house in houses:
            accounts = Accounts.objects.filter(
                street__exact=house['street'],
                house_number__exact=house['house_number']
            ).values(
                'id',
                'apartments_number'
            )

            apartments_data = {
                'house': house,
                'apartments_data': sorted([(i['apartments_number'], i['id']) for i in accounts],
                                          key=lambda x: self.str_to_num(x[0])),
            }
            apartments.append(apartments_data)
        return apartments

    def check_group(self):
        try:
            group_check = self.request.user.groups.filter(name='dispatchers').exists()
        except AttributeError:
            group_check = False
        return group_check

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            file_upload_form = FileFieldForm()
            houses = self.get_houses_list()
            houses_apartments = self.get_apartments_of_house(houses)

            context = {
                'house_apartments': houses_apartments,
                'houses': houses,
                'form': file_upload_form
            }

            return render(request, self.template, context)
        else:
            return redirect('management_login')

    def post(self, request, *args, **kwargs):
        """management logout function"""
        logout(request)
        return JsonResponse({'ok': '/management/login/'})
