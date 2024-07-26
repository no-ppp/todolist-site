from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from .models import SocialUser

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        email = user.email

        # Sprawdzanie czy email już istnieje w SocialUser
        if email:
            try:
                social_user = SocialUser.objects.get(email=email)
                # Możemy przypisać użytkownika do instancji SocialUser
                sociallogin.user = social_user
            except SocialUser.DoesNotExist:
                # Tworzenie nowego SocialUser
                social_user = SocialUser(
                    email=email,
                    username=user.username or email,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
                social_user.set_unusable_password()  # Social users may not need passwords
                social_user.save()
                sociallogin.user = social_user

        return user