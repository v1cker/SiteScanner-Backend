from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

# Create your tests here.


class RegisterSiteTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@testing.eu', password='top_secret')

    def test_register_from_snapshot_with_unregistered_user(self):
        """
        If user is unauthenticated,
        redirect to the login page
        """
        request = self.factory.get('/site_from_snapshot/')
        request.user = AnonymousUser
        response = self.client.get('/site_from_snapshot/')
        self.assertRedirects(response, expected_url='/accounts/login/', status_code=302, target_status_code=200)

