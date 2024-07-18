from django import forms
from .models import Money, TodoList

class MoneyForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = '__all__'


class MoneySearch(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)
    important_only = forms.BooleanField(label='Important only', required=False)


class EditTodo(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = [
            'task', 'important',
        ]


class IsActive(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = [
            'active'
        ]


class AddTitle(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = [
            'title'
        ]
