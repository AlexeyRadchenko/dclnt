import datetime
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from counters.forms import FileFieldForm
from .serializers import UserSerializer
from django.core.cache import cache
from django.conf import settings
from counters.tasks import load_files_data_to_db
from counters.models import Counters
from .forms import ElectricCountersForm, ElectricCountersFormDayNight, WaterCountersForm, GasCountersForm


class ListUsers(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FileUploadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        form = FileFieldForm(request.POST, request.FILES)
        data = {}
        if form.is_valid():
            """id from file_upload.js"""
            self.handle_uploaded_file(request.FILES, process_id=request.POST['id'])
            if cache.get(request.POST.get('id')):
                data['file_load'] = 'ok'
            else:
                data['file_load'] = 'not process'
        else:
            print(form)
            data['file_load'] = 'form_error'
        return Response(data)

    @staticmethod
    def handle_uploaded_file(files, process_id=None):
        files_list = []
        for f in files.getlist('file_field'):
            path_n_filename = ''.join([settings.MEDIA_ROOT, '/import/', f.name])
            with open(path_n_filename, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            files_list.append(path_n_filename)
        cache.set(process_id, 1, timeout=None)

        """вызов загрузчика данных в базу из файла"""
        load_files_data_to_db.delay(files_list, process_id)


class UpdateProgressBarView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        loading_task = cache.get(request.GET.get('id'))
        if loading_task and loading_task != 404:
            if loading_task < 100:
                return Response(data={
                    'percent': loading_task,
                    'status': 'loading',
                    'id': request.GET.get('id')})
            else:
                return Response(data={'percent': 100, 'status': 'done', 'id': request.GET.get('id')})
        else:
            return Response(data={'percent': 0, 'status': 'error', 'id': request.GET.get('id')})


class GetAccountFormAndData (APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (FormParser,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'management/acc_form_and_data.html'

    @staticmethod
    def get_account_electric_counters_data_and_form(counters):
        electric_counter_data = 'нет зарегистрированных электросчетчиков'
        electric_counter_form = None
        for counter in counters:
            if counter[0] == 'Электроэнергия':
                if counter[1]:
                    electric_counter_data = {
                        'serial_number': counter[7],
                        'date_update': counter[8],
                        'counter_data_simple': counter[1],
                        'id': counter[10],
                        'diff': counter[1] - counter[4],
                        'id_account': counter[9],
                    }
                    electric_counter_form = ElectricCountersForm()
                else:
                    electric_counter_data = {
                        'serial_number': counter[7],
                        'date_update': counter[8],
                        'counter_data_day': counter[2],
                        'counter_data_night': counter[3],
                        'id': counter[10],
                        'diff_day': counter[3]-counter[5],
                        'diff_night': counter[2]-counter[6],
                        'id_account': counter[9],
                    }
                    electric_counter_form = ElectricCountersFormDayNight()
        return electric_counter_data, electric_counter_form

    @staticmethod
    def get_account_water_counters_data_and_form(counters):
        counters_list = []
        for counter in counters:
            if 'вода' in counter[0]:
                water_counter_data = {
                    'counters_type': counter[0],
                    'serial_number': counter[7],
                    'date_update': counter[8],
                    'counter_data': counter[1],
                    'diff': counter[1] - counter[4],
                    'id': counter[10],
                    'id_account': counter[9]
                }
                counters_list.append(water_counter_data)
        if counters_list:
            return counters_list, WaterCountersForm()
        else:
            return 'нет зарегистрированных водосчетчиков', None

    @staticmethod
    def get_account_gas_counters_data_and_form(counters):
        gas_counter_data = 'нет зарегистрированных газовых счетчиков'
        gas_counter_form = None
        for counter in counters:
            if 'Газ' in counter[0]:
                gas_counter_data = {
                    'serial_number': counter[7],
                    'date_update': counter[8],
                    'counter_data_simple': counter[1],
                    'id': counter[10],
                    'diff': counter[1] - counter[4],
                    'id_account': counter[9],
                }
                gas_counter_form = GasCountersForm()

        return gas_counter_data, gas_counter_form

    def post(self, request):
        account = request.POST['account']

        account_counters = Counters.objects.values_list(
            'counter_type',
            'counter_data_simple',
            'counter_data_day',
            'counter_data_night',
            'old_counter_data_simple',
            'old_counter_data_day',
            'old_counter_data_night',
            'serial_number',
            'date_update',
            'account_id',
            'id',
        ).filter(account_id__exact=account, in_work=True)

        electric_counter_data, electric_counter_form = self.get_account_electric_counters_data_and_form(
            account_counters
        )
        water_counter_data, water_counter_form = self.get_account_water_counters_data_and_form(account_counters)
        gas_counter_data, gas_counter_form = self.get_account_gas_counters_data_and_form(account_counters)

        return Response(
            {
                'electric_counter': electric_counter_data,
                'form_electric': electric_counter_form,
                'water_counters': water_counter_data,
                'form_water': water_counter_form,
            }
        )


class SaveAccountNewData(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)
    account = None
    success_message = {
        'cid': None,
        'message': 'Показания счетчика приняты.'
    }

    error_message = {
        'cid': None,
        'message': 'Введенные показания меньше чем в прошлом периоде, '
                   'введите верные значения или обратитесь в расчетный центр по тел. 111-11-11'
    }

    def form_validator(self):
        forms_list = [ElectricCountersForm, ElectricCountersFormDayNight, WaterCountersForm, GasCountersForm]
        for num_form, form in enumerate(forms_list):
            result = form(self.request.POST)
            if result.is_valid():
                return num_form, result

    @staticmethod
    def get_old_data_simple_electric_water_gas_counters(account, counter_id):
        return Counters.objects.get(
            account_id__exact=account,
            id__exact=counter_id
        ).old_counter_data_simple

    def form_electric_data_simple_validator(self, form):
        old_data = self.get_old_data_simple_electric_water_gas_counters(self.account, form.cleaned_data['e_counter_id'])
        if old_data <= form.cleaned_data['data']:
            return True, old_data
        else:
            return False, None

    def save_simple_electric_water_gas_data(self, form, response_data):
        validator_result = self.form_electric_data_simple_validator(form)
        if validator_result[0]:
            Counters.objects.filter(
                account_id__exact=self.account,
                id__exact=form.cleaned_data['e_counter_id']
            ).update(
                counter_data_simple=form.cleaned_data['data'],
                date_update=datetime.date.today()
            )

            response_data['data1'] = form.cleaned_data['data']
            response_data['diff1'] = form.cleaned_data['data'] - validator_result[1]
            response_data['date'] = datetime.date.today().strftime('%d.%m.%Y')

        return response_data, form.cleaned_data['e_counter_id']

    def post(self, request):
        self.account = request.POST['account_id']
        request.POST._mutable = True
        del request.POST['account_id']

        form_electric_success = None
        form_electric_error = None
        form_water_error = None
        form_water_success = None
        response_data = {
            'data1': None,
            'data2': None,
            'diff1': 0,
            'diff2': 0,
            'date': None,
        }
        validate_form = self.form_validator()
        if validate_form[1]:
            response_data, counter_id = self.save_simple_electric_water_gas_data(validate_form[1], response_data)
            if validate_form[0] == 0:
                if response_data['data1']:
                    self.success_message['cid'] = counter_id
                    response_data['el_success'] = self.success_message
                else:
                    self.error_message['cid'] = counter_id
                    response_data['el_error'] = self.error_message
            elif validate_form[0] == 1:
                pass





        """electric_counter_form = ElectricCountersForm(request.POST)
        water_counter_form = WaterCountersForm(request.POST)
        electric_counter_form_daynight = ElectricCountersFormDayNight(request.POST)
        # gas_counter_form = GasCountersForm(request.POST)
        if electric_counter_form.is_valid():
            # запрашиваем значение показаний за прошлый период из базы

            old_data = ElectricCounters.objects.get(id_account_id__exact=username,
                                                    id__exact=electric_counter_form.cleaned_data[
                                                        'e_counter_id']).old_counter_data_simple
            # проверяем значения
            if old_data <= electric_counter_form.cleaned_data['data']:
                ElectricCounters.objects.filter(id_account_id__exact=username,
                                                id__exact=electric_counter_form.cleaned_data['e_counter_id']). \
                    update(counter_data_simple=electric_counter_form.cleaned_data['data'],
                           date_update=datetime.date.today(),
                           diff_simple=electric_counter_form.cleaned_data['data'] - old_data)
                response_data['data1'] = electric_counter_form.cleaned_data['data']
                response_data['diff1'] = electric_counter_form.cleaned_data['data'] - old_data
                response_data['date'] = datetime.date.today().strftime('%d.%m.%Y')
                form_electric_success = \
                    {
                        'cid': electric_counter_form.cleaned_data['e_counter_id'],
                        'message': 'Показания счетчика приняты.'
                    }
            else:
                form_electric_error = {
                    'cid': electric_counter_form.cleaned_data['e_counter_id'],
                    'message': 'Введенные показания меньше чем в прошлом периоде, введите верные значения или обратитесь в расчетный центр по тел. 6-39-87'
                }

        elif electric_counter_form_daynight.is_valid():
            # запрашиваем значение показаний за прошлый период из базы
            old_data = ElectricCounters.objects.get(id_account_id__exact=username,
                                                    id__exact=electric_counter_form.cleaned_data[
                                                        'e_counter_id'])
            # проверяем значения
            if old_data.old_counter_data_day <= electric_counter_form_daynight.cleaned_data[
                'data_day'] and old_data.old_counter_data_night <= electric_counter_form_daynight.cleaned_data[
                'data_night']:
                ElectricCounters.objects.filter(id_account_id__exact=username,
                                                id__exact=electric_counter_form.cleaned_data['e_counter_id']). \
                    update(counter_data_day=electric_counter_form_daynight.cleaned_data['data_day'],
                           counter_data_night=electric_counter_form_daynight.cleaned_data['data_night'],
                           date_update=datetime.date.today(),
                           diff_day=electric_counter_form_daynight.cleaned_data[
                                        'data_day'] - old_data.old_counter_data_day,
                           diff_night=electric_counter_form_daynight.cleaned_data[
                                          'data_night'] - old_data.old_counter_data_night)
                form_electric_success = \
                    {
                        'cid': electric_counter_form.cleaned_data['e_counter_id'],
                        'message': 'Показания счетчика приняты.'
                    }
                response_data['data1'] = electric_counter_form_daynight.cleaned_data['data_day']
                response_data['data2'] = electric_counter_form_daynight.cleaned_data['data_night']
                response_data['diff1'] = electric_counter_form_daynight.cleaned_data[
                                             'data_day'] - old_data.old_counter_data_day
                response_data['diff2'] = electric_counter_form_daynight.cleaned_data[
                                             'data_night'] - old_data.old_counter_data_night
                response_data['date'] = datetime.date.today().strftime('%d.%m.%Y')
            else:
                form_electric_error = {
                    'cid': electric_counter_form.cleaned_data['e_counter_id'],
                    'message': 'Введенные показания меньше чем в прошлом периоде, введите верные значения или обратитесь в расчетный центр по тел. 6-39-87'
                }

        elif water_counter_form.is_valid():
            old_data = WaterCounters.objects.get(id_account_id__exact=username,
                                                 id__exact=request.POST['counter_id'],
                                                 in_work__exact=True).old_counter_data
            if old_data <= water_counter_form.cleaned_data['data_water']:
                WaterCounters.objects.filter(id_account_id__exact=username,
                                             id__exact=request.POST['counter_id']). \
                    update(counter_data=water_counter_form.cleaned_data['data_water'],
                           date_update=datetime.date.today(),
                           diff=water_counter_form.cleaned_data['data_water'] - old_data)
                form_water_success = {
                    'cid': int(request.POST['counter_id']),
                    'message': 'Показания счетчика приняты.',
                }

                response_data['data1'] = water_counter_form.cleaned_data['data_water']
                response_data['diff1'] = water_counter_form.cleaned_data['data_water'] - old_data
                response_data['date'] = datetime.date.today().strftime('%d.%m.%Y')

            else:
                form_water_error = {
                    'cid': int(request.POST['counter_id']),
                    'message': 'Введенные показания меньше чем в прошлом периоде, введите верные значения или обратитесь в расчетный центр по тел. 6-39-87',
                }

        elif water_counter_form.errors:
            print(water_counter_form['data_water'].errors[0])
            if water_counter_form['data_water'].errors[0] == 'Введите дробное число':
                form_water_error = {
                    'cid': int(request.POST['counter_id']),
                    'message': 'Пожалуйста введите корректные данные: десятичная дробь с разделителем (например: 43.230 или 4.000)',
                }"""

        response_data['ok'] = 'save'
        response_data['wt_error'] = form_water_error
        response_data['wt_success'] = form_water_success
        print(response_data)
        return Response(response_data)
