from django import forms
from django.core.validators import RegexValidator

class ElectricCountersForm(forms.Form):
    data = forms.IntegerField(
        label='Введите показания счетчика',
        widget=forms.TextInput(attrs={'placeholder':'пример: 1243','class':'electricinput','type':'number','step':'1', 'min':'0', 'max': '999999'}),
    )
    e_counter_id = forms.IntegerField(widget=forms.HiddenInput())
    #form_type = forms.IntergerField(widget=forms.HiddenInput())

class ElectricCountersFormDayNight(forms.Form):
    data_day = forms.IntegerField(
        label='Введите показания счетчика(день)',
        widget=forms.TextInput(attrs={'placeholder':'пример: 1243','class':'electricinput','type':'number','step':'1', 'min':'0'}),
    )
    data_night = forms.IntegerField(
        label='Введите показания счетчика(ночь)',
        widget=forms.TextInput(attrs={'placeholder': 'пример: 456','class':'electricinput','type':'number','step':'1', 'min':'0'}),
    )
    e_counter_id = forms.IntegerField(widget=forms.HiddenInput())

class WaterCountersForm(forms.Form):
    data_water = forms.DecimalField(label='Введите показания счетчика',
                              max_digits=9, decimal_places=3,
                              widget=forms.TextInput(attrs={'placeholder': 'пример: 001234.567','class':'waterinput', 'pattern':'\d+((,|\.)\d{1,3})?'}),
                              localize=True,
                              validators=[RegexValidator(regex='\d+\.\d{1,3}|\d+\,\d{1,3}',message='Введите дробное число', code='not double')],
    )
    counter_id = forms.IntegerField(widget=forms.HiddenInput())


class GasCountersForm(forms.Form):
    data_gas = forms.DecimalField(label='Введите показания счетчика',
                              max_digits=9, decimal_places=3,
                              widget=forms.TextInput(attrs={'placeholder': 'пример: 001234.567','class':'gasinput', 'pattern':'\d+((,|\.)\d{1,3})?'}),
                              localize=True,
                              validators=[RegexValidator(regex='\d+\.\d{1,3}|\d+\,\d{1,3}',message='Введите дробное число', code='not double')],
    )

    g_counter_id = forms.IntegerField(widget=forms.HiddenInput())


class NoAccessForm(forms.Form):
    email = forms.EmailField(
        max_length = 40,
        widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Ваш email'}),
    )
    account = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Лицевой счет'})
    )
    street = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица'})
    )
    house = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер дома'})
    )
    apartments = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Квартира'})
    )