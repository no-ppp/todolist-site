from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from Google import sending_message


def send_activation_token(user):
    sender = settings.DEFAULT_FROM_EMAIL
    to = user.email
    subject = 'Activate Your Account'
    message_text = (f'Hello Dear {user.username}. \n'
                    f'Here is your activation link: '
                    f'{settings.SITE_URL}/activate/{user.activation_token}')
    # Sending message
    sending_message(
        sender,
        to,
        subject,
        message_text,
    )