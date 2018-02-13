from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from counters.models import Counters, Accounts
from api_v0.forms import ElectricCountersForm, ElectricCountersFormDayNight, WaterCountersForm, GasCountersForm


class AccountsLoginView(TemplateView):
    template_name = 'accounts/login.html'

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        street, house_number, apartments = Accounts.objects.values_list(
            'street',
            'house_number',
            'apartments_number'
        ).filter(
            user__exact=request.POST['username']
        )[0]

        if street == request.POST['street'] and house_number == request.POST['house_number']\
                and apartments == request.POST['apartments_number']:
            if user is not None:
                login(request, user)
                return JsonResponse({'ok': '/accounts/{}/'.format(user)})
            else:
                return JsonResponse({'error': 'неверный логин или пароль'})
        else:
            JsonResponse({'error': 'неверный адрес'})


class AccountsView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/profile.html'
    account = None
    login_url = '/accounts/login/'

    def get_account_counters(self):
        return Counters.objects.values_list(
            'counter_type',
            'counter_data_simple',
            'counter_data_day',
            'counter_data_night',
            'old_counter_data_simple',
            'old_counter_data_day',
            'old_counter_data_night',
            'serial_number',
            'date_update',
            'id',
            'account_id'
        ).filter(
            account_id__exact=self.account,
        )

    def get_account_address(self):
        return Accounts.objects.values_list(
            'street',
            'house_number',
            'apartments_number',
        ).filter(
            user__exact=self.account
        )

    @staticmethod
    def get_electric_counter_data_and_form(account_counters):
        electric_counters_data, electric_counter_form = None, None
        for counter in account_counters:
            if counter[0] == 'Электроэнергия':
                if counter[1]:
                    electric_counters_data = {
                        'serial_number': counter[7],
                        'date_update': counter[8],
                        'counter_data_simple': counter[1],
                        'id': counter[9],
                        'diff': counter[1]-counter[4],
                        'account_id': counter[10],
                    }
                    electric_counter_form = ElectricCountersForm()
                    break
                else:
                    electric_counters_data = {
                        'serial_number': counter[7],
                        'date_update': counter[8],
                        'counter_data_day': counter[2],
                        'counter_data_night': counter[3],
                        'id': counter[9],
                        'diff_day': counter[2] - counter[5],
                        'diff_night': counter[3] - counter[6],
                        'account_id': counter[10],
                    }
                    electric_counter_form = ElectricCountersFormDayNight()
                    break
        if electric_counters_data is None:
            electric_counters_data = 'нет зарегистрированных электросчетчиков'
        return electric_counters_data, electric_counter_form

    @staticmethod
    def get_water_counters_data_and_form(account_counters):
        water_counters_data, water_counter_form = [], None
        for counter in account_counters:
            if 'вода' in counter[0]:
                data = {
                    'counters_type': counter[0],
                    'serial_number': counter[7],
                    'date_update': counter[8],
                    'counter_data': counter[1],
                    'id': counter[9],
                    'diff': counter[1] - counter[4],
                    'account_id': counter[10],
                }
                water_counters_data.append(data)
        if water_counters_data:
            water_counter_form = WaterCountersForm()
        else:
            water_counter_form = 'нет зарегистрированных водосчетчиков'
        return water_counters_data, water_counter_form

    @staticmethod
    def get_gas_counter_data_and_form(account_counters):
        gas_counter_data, gas_counter_form = None, None
        for counter in account_counters:
            if 'Газ' in counter[0]:
                gas_counter_data = {
                    'counters_type': counter[0],
                    'serial_number': counter[7],
                    'date_update': counter[8],
                    'counter_data': counter[1],
                    'id': counter[9],
                    'diff': counter[1] - counter[4],
                    'account_id': counter[10],
                }
                break
        if gas_counter_data is None:
            gas_counter_form = 'нет зарегистрированных газовых счетчиков'
        else:
            gas_counter_form = WaterCountersForm()
        return gas_counter_data, gas_counter_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.account = self.kwargs['username']
        account_counters = self.get_account_counters()
        electric_counters_data, electric_counter_form = self.get_electric_counter_data_and_form(account_counters)
        water_counters_data, water_counters_form = self.get_water_counters_data_and_form(account_counters)
        gas_counter_data, gas_counter_form = self.get_gas_counter_data_and_form(account_counters)
        address = self.get_account_address()

        context['username'] = self.account
        context['id'] = self.account
        context['address'] = f'ул. {address[0][0]}, д. {address[0][1]}, кв. {address[0][2]}'
        context['electric_counter'] = electric_counters_data
        context['water_counters'] = water_counters_data
        context['gas_counter'] = gas_counter_data
        context['form_electric'] = electric_counter_form
        context['form_water'] = None if isinstance(water_counters_form, str) else water_counters_form
        context['form_gas'] = None if isinstance(gas_counter_form, str) else gas_counter_form
        context['display_electric'] = True

        return context


class AccountsLogoutView(TemplateView):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)
