from django import forms
from .models import Money, TodoList, TitleTodo, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError




class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class MoneyForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = '__all__'


class MoneySearch(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)
    important_only = forms.BooleanField(label='Important only', required=False)


class TodoTitleForm(forms.ModelForm):
    class Meta:
        model = TitleTodo
        fields = ['title']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


    def clean_title(self):
        user = self.user
        title = self.cleaned_data.get('title')
        if TitleTodo.objects.filter(title=title, user=user).exists():
            raise ValidationError(f'The title "{title}" already exists for this user.')
        return title

    


class EditTodoForm(forms.ModelForm):
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


class AddTitleForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['title'].queryset = TitleTodo.objects.filter(user=user)
