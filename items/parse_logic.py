import csv
from typing import Any

from django.core.exceptions import ObjectDoesNotExist

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
    first_header_name = 'Код'
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        if row[table_header_indexes_dict['article']] == first_header_name:
            continue
        create_or_update_item(row)


def create_or_update_item(item_values_list: list[str]) -> None:
    item_values_dict = get_item_values_dict(item_values_list)
    first_column_name = 'article'

    try:
        item = Item.objects.get(article=item_values_dict[first_column_name])
    except ObjectDoesNotExist:
        item = Item(article=item_values_dict[first_column_name])

    for key, value in item_values_dict.items():
        if key == first_column_name:
            continue
        elif key in table_header_indexes_dict:
            setattr(item, key, value)
    item.save()


def get_item_values_dict(item_values_list: list[str]) -> dict[str, Any]:
    item_values_dict = dict()

    item_values_dict['article'] = item_values_list[table_header_indexes_dict['article']]
    item_values_dict['name'] = item_values_list[table_header_indexes_dict['name']]

    category_1_name = item_values_list[table_header_indexes_dict['category_1']]
    category_2_name = item_values_list[table_header_indexes_dict['category_2']]
    category_3_name = item_values_list[table_header_indexes_dict['category_3']]
    category_1, category_2, category_3 = get_categories_or_create_new((category_1_name, category_2_name,
                                                                       category_3_name))
    item_values_dict['category_1'] = category_1
    item_values_dict['category_2'] = category_2
    item_values_dict['category_3'] = category_3

    item_values_dict['price'] = get_float_or_none_from_values_list('price', item_values_list)
    item_values_dict['price_sp'] = get_float_or_none_from_values_list('price_sp', item_values_list)
    item_values_dict['quantity'] = get_float_or_none_from_values_list('quantity', item_values_list)
    item_values_dict['property_fields'] = item_values_list[table_header_indexes_dict['property_fields']]
    item_values_dict['joint_purchase'] = item_values_list[table_header_indexes_dict['joint_purchase']]

    unit_of_measurement_name = item_values_list[table_header_indexes_dict['unit_of_measurement']]
    item_values_dict['unit_of_measurement'] = get_unit_of_measurement_or_create_new(unit_of_measurement_name)

    item_values_dict['image'] = item_values_list[table_header_indexes_dict['image']]
    item_values_dict['is_on_the_main_page'] = item_values_list[table_header_indexes_dict['is_on_the_main_page']]

    if len(item_values_list) > len(table_header_indexes_dict):
        item_values_dict['description'] = ';'.join(item_values_list[table_header_indexes_dict['description']:])
    else:
        item_values_dict['description'] = item_values_list[table_header_indexes_dict['description']]

    return item_values_dict


def get_categories_or_create_new(category_names: tuple[str, str, str]) -> list[Any | None]:
    category_models = {
        0: CategoryOne,
        1: CategoryTwo,
        2: CategoryThree,
    }
    category_list = []

    for i in range(len(category_names)):
        name = category_names[i]
        if not name:
            category = None
        else:
            if not category_list:
                category_set = category_models[i].objects.filter(name=name)
            else:
                parent_category = category_list[i - 1]
                category_set = category_models[i].objects.filter(name=name, parent_category=parent_category)
            if category_set.count() == 0:
                if not category_list:
                    category = category_models[i].objects.create(name=name)
                else:
                    category = category_models[i].objects.create(name=name, parent_category=parent_category)
            else:
                category = category_set.first()
        category_list.append(category)
    return category_list


def get_float_or_none_from_values_list(name_field: str, values_list: list[Any]) -> float | None:
    value = values_list[table_header_indexes_dict[name_field]].replace(',', '.')
    value = float(value) if value else None
    return value


def get_unit_of_measurement_or_create_new(unit_of_measurement_name: str) -> UnitOfMeasurement:
    try:
        unit_of_measurement = UnitOfMeasurement.objects.get(name=unit_of_measurement_name)
    except ObjectDoesNotExist:
        unit_of_measurement = UnitOfMeasurement.objects.create(name=unit_of_measurement_name)

    return unit_of_measurement
