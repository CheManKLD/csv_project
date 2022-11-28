from django import forms
from django.core.validators import FileExtensionValidator


class UploadCSVFileForm(forms.Form):
    csv_file = forms.FileField(label='CSV файл', validators=[FileExtensionValidator(allowed_extensions=['csv'],
                                                                                    message='Неверный формат файла')])
