import io

from django.shortcuts import render
from django.views.generic import ListView

from .forms import UploadCSVFileForm
from .models import Item
from .parse_logic import parse_csv_file_of_items

headers_of_table = (
    'Код',
    'Наименование',
    'Уровень1',
    'Уровень2',
    'Уровень3',
    'Цена',
    'ЦенаСП',
    'Количество',
    'Поля свойств',
    'Совместные покупки',
    'Единица измерения',
    'Картинка',
    'Выводить на главной',
    'Описание',
)


def items_main(request):
    context = {'title': 'Главная страница'}
    return render(request, 'items/main.html', context)


def upload_csv_file(request):
    message = 'Загрузите CSV файл с товарами'
    if request.method == 'POST':
        form = UploadCSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            parse_csv_file_of_items(io_string)
            message = 'Файл успешно обработан'
    else:
        form = UploadCSVFileForm()

    context = {'form': form, 'message': message, 'title': 'Страница загрузки CSV файла товаров'}
    return render(request, 'items/upload_file.html', context)


class ItemsListView(ListView):
    paginate_by = 30
    model = Item
    template_name = 'items/items_list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список товаров'
        context['headers_of_table'] = headers_of_table
        return context
