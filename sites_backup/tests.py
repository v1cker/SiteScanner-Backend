from django.test import TestCase, Client
from django.contrib.auth.models import User


def create_and_login_test_user(user_name='test', password='abc123de'):
    client = Client()
    user = User.objects.create_user(user_name, 'test@testing.eu', password)
    user.save()
    client.login(username='test', password='abc123de')
    return client


class DownloadSiteTests(TestCase):

    def test_download_site_with_unregistered_user(self):
        """
        If user is unauthenticated,
        redirect to the login page
        """
        response = self.client.get('/download_site/1/')
        self.assertRedirects(response, expected_url='/accounts/login/', status_code=302, target_status_code=200)

    def test_download_site_with_not_given_site_id(self):
        """
        If site_id was not given as an argument,
        user should see rendered error page.
        """
        self.client = create_and_login_test_user()
        response = self.client.get('/download_site/')
        self.assertTemplateUsed(response, template_name='register_site/error_page.html')
