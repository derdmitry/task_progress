from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Target


class TargetForm(forms.ModelForm):

    class Meta:
        model = Target
        fields = ['target_description', 'target', 'start_date', 'end_date', 'done', 'priority']
        exclude = ('user',)
        start_date = forms.DateField(localize=True)

        labels = {
            'target_description': 'Описание цели',
            'target': 'Сколько сделать',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'done': 'Уже сделано',
            'priority': 'Приоритет',
        }

        widgets = {'start_date': forms.DateInput(attrs={'id': 'start_date'}),
                   'end_date': forms.DateInput(attrs={'id': 'end_date'}),
        }



class AddProgressForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['done', ]
        exclude = ('user', 'target_description', 'target', 'start_date', 'end_date', 'priority' )
        labels = {
            'done': 'Уже сделано',

        }

#for registration
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password')

