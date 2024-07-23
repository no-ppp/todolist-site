from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True,blank=True)
    avatar = models.ImageField(null=True, default="Avatarwander.png")


class Money(models.Model):
    CHOICES_TYPE = [
        ('billings', 'Billings'),
        ('earnings', 'Earnings'),
    ]
    field_info = models.CharField(max_length=50)
    what_info = models.CharField(max_length=50)
    type_info = models.CharField(max_length=20, choices=CHOICES_TYPE, default='billings')
    important_info = models.BooleanField(verbose_name='Is this important ?', default=False)
    created_at = models.DateTimeField(auto_now=True)
    money_info = models.FloatField(verbose_name='Money')

    def __str__(self) -> str:
        return f"{self.field_info} - {self.what_info} - {self.money_info} zł"
    

class TitleTodo(models.Model):
    title = models.CharField(max_length=30)   
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    class Meta:
        unique_together = ('title', 'user')

    def __str__(self) -> str:
        return self.title
    

class TodoList(models.Model):
    title = models.ForeignKey(TitleTodo, on_delete=models.CASCADE)
    task = models.CharField(max_length=20)
    important = models.BooleanField(verbose_name='Is it important ?', default=False)
    active = models.BooleanField(verbose_name="Mark if it's uncompleted", default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.task} - {self.important} - {self.active}"