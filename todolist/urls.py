from django.urls import path
from . import views


app_name = 'todolist'

urlpatterns = [
    path('', views.home, name='home'),
    path('login_view/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('register_completed/', views.register_completed, name='register_completed'),
    path('password_reset_email/', views.password_reset, name='password_reset_email' ),
    path('new_password_email/<str:uidb64>/<str:token>/', views.new_password_email, name='new_password_email'),
    path('new_password_invalid/', views.new_password_invalid, name='new_password_invalid'),
    path('password_reset_done/<str:uidb64>/', views.password_reset_done, name='password_reset_done'),
    path('invalid_email/', views.invalid_email, name='invalid_email'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('required_active_user/', views.required_active_view, name='required_active_user'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:user_id>/', views.profile, name='profile'),
    path('money_view/<int:user_id>/', views.money_view, name='money_view'),
    path('money_view_add/<int:user_id>/', views.money_view_add, name='money_view_add'),
    path('todo_view/<int:user_id>/', views.todo_view, name='todo_view'),
    path('profile_settings/<int:user_id>/', views.profile_settings, name='profile_settings'),
    path('add_todo_title/<int:user_id>/', views.add_title_todo, name= 'add_title_todo'),
    path('add_todo_with_title/<int:user_id>', views.add_todo_with_title, name='add_todo_with_title'),
    path('delete_task/<int:user_id>/<int:todolist_id>/', views.delete_task, name='delete_task'),
    path('set_completed/<int:user_id>/<int:todolist_id>/', views.set_completed, name='set_completed'),
    path('edit_task/<int:user_id>/<int:todolist_id>', views.edit_task, name='edit_task'),
    path('edit_current_task/<int:user_id>/<int:title_id>/', views.edit_current_task, name='edit_current_task'),
    path('activate/<str:token>/', views.activation_user, name='activate'),
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),
]

