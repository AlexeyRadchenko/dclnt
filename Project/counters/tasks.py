from __future__ import absolute_import, unicode_literals
from celery import shared_task
from dataexchanger.importers import DataLoader


@shared_task
def load_files(files_list, process_id):
    DataLoader(files_list, process_id)
