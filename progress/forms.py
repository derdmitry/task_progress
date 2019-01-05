from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Target


class TargetForm(forms.ModelForm):
    # target_description = forms.CharField(widget=forms.Textarea(attrs={'class':'widget_descr'}), max_length=200)

    def clean(self):
        cleaned_data = super(TargetForm, self).clean()
        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise forms.ValidationError("Как может быть дата начала позже даты окончания? Исправляем.", code="invalid")

        # if cleaned_data['target'] < 0:
        #     raise forms.ValidationError("Отрицательная цель выглядит странно. Испрааляем.", code="invalid")

        return cleaned_data

    class Meta:
        model = Target
        fields = ['target_description', 'target', 'start_date', 'end_date', 'done', 'priority']
        # exclude = ('user',)
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
                   'target_description': forms.Textarea(attrs={'class': 'widget_descr'}),
                   }


class AddProgressForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['done', ]
        exclude = ('user', 'target_description', 'target', 'start_date', 'end_date', 'priority')
        labels = {
            'done': 'Уже сделано',

        }


# for registration
class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password')
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'email': 'E-mail',
            'password': 'Пароль',
        }

        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                   }

        help_texts = {'username': 'Буквы, цифры и символы _, @, +, . - '
                      }
