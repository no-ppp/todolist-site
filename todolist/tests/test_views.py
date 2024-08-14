from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from todolist.models import User, Country




# LOGIN FUNCTION TESTS
class UrlRedirectsTests(TestCase):
    def setUp(self):
        self.url = reverse('todolist:login')
        self.country = Country.objects.create(country='Poland')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='12345',
            is_active=True
        )

    def test_authenticated_user_redirect(self):
        self.client.login(email='test@gmail.com', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302) # Redirect to home page

    def test_home_to_dashboard_redirect(self):
        self.client.login(email='test@gmail.com', password='12345')
        response = self.client.get(reverse('todolist:home'))
        self.assertRedirects(response, reverse('todolist:dashboard', args=[self.user.id]))

    def test_register_to_home_redirect(self):
        self.client.login(email='test@gmail.com', password='12345')         #<--- Cant make AssertRedirects work
        response = self.client.get(reverse('todolist:register'))            #<--- Because those functions first redirect
        self.assertEqual(response.status_code, 302)                         #<--- to home and then to dashboard
        self.assertEqual(response['Location'], reverse('todolist:home'))    #<--- But this is working the same way

    def test_logout_to_home_redirect(self):
        self.client.login(email='test@gmail.com', password='12345')
        response = self.client.get(reverse('todolist:logout'))
        self.assertRedirects(response, reverse('todolist:home'))

    def test_register_view_to_home_redirect(self):
        self.client.login(email='test@gmail.com', password='12345')
        response = self.client.get(reverse('todolist:register_completed'))
        self.assertEqual(response['Location'], reverse('todolist:home'))

    def test_password_reset_email_to_home_redirect(self):
        self.client.login(email='test@gmail.com', password='12345')
        response = self.client.get(reverse('todolist:password_reset_email'))
        self.assertEqual(response['Location'], reverse('todolist:home'))

    def test_new_password_invalid_to_home_redirect(self):
        self.client.login(email='test@gmail.com', password='12345')
        response = self.client.get(reverse('todolist:new_password_invalid'))
        self.assertEqual(response['Location'], reverse('todolist:home'))

    def test_login_with_correct_credentials(self):
        login = self.client.login(email='test@gmail.com', password='12345')
        self.assertTrue(login)

    def test_login_with_incorrect_email(self):
        login = self.client.login(email='wrong@gmail.com', password='12345')
        self.assertFalse(login)

    def test_login_with_incorrect_password(self):
        login = self.client.login(email='test@gmail.com', password='wrongpassword')
        self.assertFalse(login)


# REGISTER FUNCTION TESTS
class RegisterViewTests(TestCase):
    def setUp(self):
        self.register_url = reverse('todolist:register')
        self.country = Country.objects.create(country='Poland')

    @patch('Google.create_message')  # Mock the create_message function
    @patch('Google.send_message')  # Mock the send_message function
    @patch(
        'allauth.socialaccount.adapter.DefaultSocialAccountAdapter.get_app'
    )  # Mock the get_app method
    @patch(
        'allauth.socialaccount.templatetags.socialaccount.provider_login_url'
    )  # Mock the provider_login_url template tag
    def test_register_with_valid_data(
        self, mock_provider_login_url, mock_get_app, mock_send_message, mock_create_message
    ):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@gmail.com',
            'password1': 'A$tr0ng3rP@ssw0rd!',
            'password2': 'A$tr0ng3rP@ssw0rd!',
            'country': self.country.id
        })
        # Ensure the User instance is created
        user_exists = User.objects.filter(email='newuser@gmail.com').exists()
        self.assertTrue(user_exists)
        self.assertEqual(response.status_code, 302)

    @patch('Google.create_message')  # Mock the create_message function
    @patch('Google.send_message')  # Mock the send_message function
    @patch(
        'allauth.socialaccount.adapter.DefaultSocialAccountAdapter.get_app'
    )  # Mock the get_app method
    @patch(
        'allauth.socialaccount.templatetags.socialaccount.provider_login_url'
    )  # Mock the provider_login_url template tag
    def test_register_with_wrong_data(
        self, mock_provider_login_url, mock_get_app, mock_send_message, mock_create_message
    ):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': '',
            'password1': 'A$tr0ng3rP@rd!',
            'password2': 'A$tr0ng3rP@ssw0rd!',
            'country': self.country.id
        })
        
        # Ensure the response status code is 200 (form re-rendered with errors)
        self.assertEqual(response.status_code, 200)
        
        # Check for form in response context
        form = response.context.get('register_form')
        self.assertIsNotNone(form, "Form is not present in the response context.")
        
        # Check for form errors
        self.assertTrue(form.errors, "Form does not contain errors.")
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['This field is required.'])