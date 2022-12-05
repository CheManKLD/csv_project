import csv
from typing import Any

from items.models import CategoryOne, CategoryTwo, CategoryThree, Item, UnitOfMeasurement

table_header_indexes_dict = {
    'article': 0,
    'name': 1,
    'category_1': 2,
    'category_2': 3,
    'category_3': 4,
    'price': 5,
    'price_sp': 6,
    'quantity': 7,
    'property_fields': 8,
    'joint_purchase': 9,
    'unit_of_measurement': 10,
    'image': 11,
    'is_on_the_main_page': 12,
    'description': 13,
}


def parse_csv_file_of_items(file) -> None:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Пропускает строку с заголовками таблицы
    for row in reader:
        create_or_update_item(row)


def create_or_update_item(item_values_list: list[str]) -> None:
    item_values_dict = get_item_values_dict(item_values_list)
    article = item_values_dict.pop('article')
    Item.objects.update_or_create(article=article, defaults=item_values_dict)


def get_item_values_dict(item_values_list: list[str]) -> dict[str, Any]:
    item_values_dict = dict()

    item_values_dict['article'] = item_values_list[table_header_indexes_dict['article']]
    item_values_dict['name'] = item_values_list[table_header_indexes_dict['name']]

    category_1_name = item_values_list[table_header_indexes_dict['category_1']]
    category_1, _ = CategoryOne.objects.get_or_create(
        name=category_1_name
    ) if category_1_name else (None, None)

    category_2_name = item_values_list[table_header_indexes_dict['category_2']]
    category_2, _ = CategoryTwo.objects.get_or_create(
        name=category_2_name, parent_category=category_1
    ) if category_2_name else (None, None)

    category_3_name = item_values_list[table_header_indexes_dict['category_3']]
    category_3, _ = CategoryThree.objects.get_or_create(
        name=category_3_name, parent_category=category_2
    ) if category_3_name else (None, None)

    item_values_dict['category_1'] = category_1
    item_values_dict['category_2'] = category_2
    item_values_dict['category_3'] = category_3

    item_values_dict['price'] = get_float_or_none_from_values_list('price', item_values_list)
    item_values_dict['price_sp'] = get_float_or_none_from_values_list('price_sp', item_values_list)
    item_values_dict['quantity'] = get_float_or_none_from_values_list('quantity', item_values_list)
    item_values_dict['property_fields'] = item_values_list[table_header_indexes_dict['property_fields']]
    item_values_dict['joint_purchase'] = item_values_list[table_header_indexes_dict['joint_purchase']]

    unit_of_measurement_name = item_values_list[table_header_indexes_dict['unit_of_measurement']]
    unit_of_measurement, _ = UnitOfMeasurement.objects.get_or_create(name=unit_of_measurement_name)
    item_values_dict['unit_of_measurement'] = unit_of_measurement

    item_values_dict['image'] = item_values_list[table_header_indexes_dict['image']]
    item_values_dict['is_on_the_main_page'] = item_values_list[table_header_indexes_dict['is_on_the_main_page']]

    if len(item_values_list) > len(table_header_indexes_dict):
        item_values_dict['description'] = ';'.join(item_values_list[table_header_indexes_dict['description']:])
    else:
        item_values_dict['description'] = item_values_list[table_header_indexes_dict['description']]

    return item_values_dict


def get_float_or_none_from_values_list(name_field: str, values_list: list[Any]) -> float | None:
    value = values_list[table_header_indexes_dict[name_field]].replace(',', '.')
    value = float(value) if value else None
    return value
