from django.dispatch import receiver
from django.contrib.auth import user_login_failed


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    email = credentials.get('email')
    username = request.get('username')
    print(f'Failed to log in {username}')

    