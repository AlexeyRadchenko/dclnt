from django.http import JsonResponse
from django.shortcuts import render
from counters.tasks import load_files_data_to_db
from .forms import FileFieldForm
from django.conf import settings
from django.core.cache import cache


"""USer django-debug-toolbar"""
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

def update_progress_bar(request):
    if cache.get(request.GET.get('id')):
        if cache.get(request.GET.get('id')) < 100:
            return JsonResponse(data={
                'percent': cache.get(request.GET.get('id')),
                'status': 'loading',
                'id': request.GET.get('id')})
        else:
            return JsonResponse(data={'percent': 100, 'status': 'done', 'id': request.GET.get('id')})
    else:
        return JsonResponse(data={'percent': 0, 'status': 'error', 'id': request.GET.get('id')})


def test(request):
    form = FileFieldForm(request.POST, request.FILES)
    if request.method == 'GET':
        return render(request, 'counters/test.html', {'form': form})
    else:
        data = {}
        if form.is_valid():
            """id from file_upload.js"""
            handle_uploaded_file(request.FILES, process_id=request.POST['id'])
            if cache.get(request.POST.get('id')):
                data['file_load'] = 'ok'
            else:
                data['file_load'] = 'not process'
        else:
            data['file_load'] = 'form_error'
        return JsonResponse(data)
