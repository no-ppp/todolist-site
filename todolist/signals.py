from django.dispatch import receiver
from django.contrib.auth import user_login_failed
from django.db.models.signals import post_save
from .models import User, TitleTodo, TodoList
from .utils import send_activation_token
from django.contrib.auth import get_user_model


@receiver(post_save, sender=User)
def create_initaial_todo_for_new_user(sender, instance, created, **kwargs):
    if created:
        title = TitleTodo.objects.create(title="Home", user=instance)
        TodoList.objects.create(title=title, task='Create New notes !', user=instance)

@receiver(post_save, sender=User)
def send_verification_link(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        send_activation_token(instance)
        
        