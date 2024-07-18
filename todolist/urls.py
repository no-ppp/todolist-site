from django.urls import path
from . import views


app_name = 'todolist'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('money_view/', views.money_view, name='money_view'),
    path('money_view_add/', views.money_view_add, name='money_view_add'),
    path('todo_view/<int:user_id>/', views.todo_view, name='todo_view'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('add_todo_with_title/<int:user_id>', views.add_todo_with_title, name='add_todo_with_title'),
    path('delete_task/<int:user_id>/<int:todolist_id>/', views.delete_task, name='delete_task'),
    path('set_completed/<int:user_id>/<int:todolist_id>/', views.set_completed, name='set_completed'),
    path('edit_task/<int:user_id>/<int:todolist_id>', views.edit_task, name='edit_task'),
    path('edit_current_task/<int:user_id>/<int:title_id>/', views.edit_current_task, name='edit_current_task')
]