from django.urls import path

from .views import *

urlpatterns = [
    path('', items_main, name='main'),
    path('uploadcsv', upload_csv_file, name='upload_file'),
    path('items', ItemsListView.as_view(), name='items_list'),
]
