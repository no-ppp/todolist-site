from django.contrib import admin
from .models import Money, TodoList, TitleTodo, User


admin.site.register(User)
admin.site.register(Money)
admin.site.register(TodoList)
admin.site.register(TitleTodo)


