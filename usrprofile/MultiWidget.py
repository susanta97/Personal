import datetime
from django import forms
from django.db import models
YEAR_CHOICES = [(year, year) for year in range(2000,  datetime.date.today().year + 1)]
MONTH_CHOICE = [(month, month) for month in range(1, 13)]

class MyMultiWidget(forms.MultiWidget):
    def __init__(self,attrs=None,*args,**kwargs):
        widgets = (

            forms.Select(attrs={}, choices=YEAR_CHOICES),
            forms.Select(attrs=attrs, choices=MONTH_CHOICE),

        )
        super(MyMultiWidget, self).__init__(widgets,*args,**kwargs)

    def decompress(self, value):
        if value:
            return value.split("-")
        return ['', '']

    # def value_from_datadict(self, data, files, name):
    #     print(super().value_from_datadict(data, files, name))
    #     day, month, = super().value_from_datadict(data, files, name)
    #
    #     return '{}-{}'.format(month, day)

class MyMultiValueField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (

            forms.CharField(required=False ),
            forms.CharField(required=False),

        )
        super(MyMultiValueField, self).__init__(fields, *args, **kwargs)
        self.widget = MyMultiWidget()

    def compress(self, data_list):
        if data_list:
            print(data_list)
            return '-'.join(data_list)

class MyTestField(models.Field):
    def formfield(self, **kwargs):
        return super(MyTestField, self).formfield(form_class=MyMultiValueField)