from django.contrib.auth.models import User

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from counters.forms import FileFieldForm
from .serializers import UserSerializer
from django.core.cache import cache
from django.conf import settings
from counters.tasks import load_files_data_to_db

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
        if cache.get(request.GET.get('id')):
            if cache.get(request.GET.get('id')) < 100:
                return Response(data={
                    'percent': cache.get(request.GET.get('id')),
                    'status': 'loading',
                    'id': request.GET.get('id')})
            else:
                return Response(data={'percent': 100, 'status': 'done', 'id': request.GET.get('id')})
        else:
            return Response(data={'percent': 0, 'status': 'error', 'id': request.GET.get('id')})