from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data=None):
        user = super().populate_user(request, sociallogin, data)
        user.is_active = True
        return user
