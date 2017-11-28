from django.http import JsonResponse
from django.shortcuts import render
from .forms import FileFieldForm
from django.conf import settings
from dataexchanger.loaders import FileReader, DataLoader


"""USer django-debug-toolbar"""
def handle_uploaded_file(files):
    files_list = []
    for f in files.getlist('file_field'):
        path_n_filename = ''.join([settings.MEDIA_ROOT, '/import/', f.name])
        with open(path_n_filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        files_list.append(path_n_filename)
    """вызов загрузчика данных в базу из файла"""

    #print('three', FileReader(files_list).result)
    print('four', DataLoader(files_list).load())
    #print(files_list) #path_n_filename.rsplit('.', 1)[1]


def update_progress_bar(request):
    if request.method == 'GET' and request.GET.get('state'):
        #print(request.GET['state'])
        if int(request.GET['state']) < 100:
            progress = int(request.GET['state'])+1
            return JsonResponse(data={'data_progress': progress})
        else:
            return JsonResponse(data={'data_progress': 101, 'cache': 'erase'})
    else:
        return JsonResponse(data={'data_progress': 101, 'cache': 'erase'})


def test(request):
    form = FileFieldForm(request.POST, request.FILES)
    #print(FileReader(['text.xls']).xls_reader())
    if request.method == 'GET':
        return render(request, 'counters/test.html', {'form': form})
    else:
        if form.is_valid():
            handle_uploaded_file(request.FILES)
            files = request.FILES.getlist('file_field')
            for file in files:
                print(file)

            data = {'is_valid': True, 'name': 'asd', 'url': '/'}

        else:
            #print(form.errors)
            data = {'is_valid': False}
        return JsonResponse(data)
