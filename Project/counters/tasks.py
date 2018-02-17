from __future__ import absolute_import, unicode_literals
from celery import shared_task
from dataexchanger.importers import DataLoader
from dataexchanger.exporters import DataUnloader


@shared_task
def load_files_data_to_db(files_list, process_id):
    DataLoader(files_list, process_id).start_loading()


@shared_task
def unload_data_to_file_from_db(file_name, file_extension, process_id, counters_type, month, year):
    DataUnloader(file_extension,  process_id, month, year, file_name=file_name, counters_type=counters_type).unload()
