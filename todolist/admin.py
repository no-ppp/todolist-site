from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Money, TodoList, TitleTodo

class UserAdminPanel(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'name', 'bio', 'avatar', 'password', 'activation_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'bio', 'avatar', 'password1', 'password2', 'activation_token'),
        }),
    )

    # Dodatkowe opcje wyświetlania w listach
    list_display = ('username', 'email', 'name', 'avatar', 'is_staff')
    search_fields = ('email', 'name')
    ordering = ('email',)


admin.site.register(User, UserAdminPanel)
admin.site.register(Money)
admin.site.register(TodoList)
admin.site.register(TitleTodo)