from django.db import models


class CategoryOne(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items_category_one'


class CategoryTwo(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    parent_category = models.ForeignKey(CategoryOne, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items_category_two'


class CategoryThree(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    parent_category = models.ForeignKey(CategoryTwo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items_category_three'


class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=10, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items_unit_of_measurement'


class Item(models.Model):
    article = models.CharField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False)
    category_1 = models.ForeignKey(CategoryOne, on_delete=models.SET_NULL, blank=True, null=True)
    category_2 = models.ForeignKey(CategoryTwo, on_delete=models.SET_NULL, blank=True, null=True)
    category_3 = models.ForeignKey(CategoryThree, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    price_sp = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    property_fields = models.CharField(max_length=510, blank=True)
    joint_purchase = models.CharField(max_length=255, blank=True)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.PROTECT, blank=False)
    image = models.ImageField(upload_to='images/items/', blank=True)
    is_on_the_main_page = models.BooleanField(default=False)
    description = models.TextField(max_length=15300, blank=True)

    def get_all_category_values(self):
        return self.category_1, self.category_2, self.category_3

    def get_all_prices(self):
        return self.price, self.price_sp

    def get_quantity_as_integer_or_with_remainder(self):
        if self.quantity % 1 == 0:
            return int(self.quantity)
        return self.quantity

    def get_integer_from_is_on_the_main_page_field(self):
        return int(self.is_on_the_main_page)

    def __str__(self):
        return f'{self.article} {self.name}'
