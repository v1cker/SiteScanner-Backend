from django.test import TestCase
from django.contrib.auth.models import User
from register_site.models import SitesIndex, RegisterSite
from scanner_engine.models import ScannerEngineSite

# Create your tests here.


class PageDetailsTests(TestCase):

    def setUp(self):
        # Set up a user
        user = User.objects.create_user("test", 'random@rand.eu', "abc123de")
        user.save()
        self.client.login(username='test', password='abc123de')
        # Add site to DB for testing purposes
        site_index = SitesIndex(
            id=1,
            alias="Test site",
            owner_username="test",
            url="test.com",
            page=1
        )
        site_index.save()
        site_data = RegisterSite(
            alias=site_index.alias,
            site_id=site_index.id,
            url=site_index.url,
            title="test title",
            description="test description",
            h1="test h1",
            timestamp="now",
            updated="now"
        )
        site_data.save()
        site_scanner = ScannerEngineSite(
            site_id=site_index.id,
            url=site_index.url,
            status_code=200,
            title=site_data.title,
            description=site_data.description,
            h1=site_data.h1,
            timestamp=site_data.timestamp
        )
        site_scanner.save()

    def test_page_details_with_unregistered_user(self):
        """
        If user is unauthenticated,
        redirect to the login page.
        """
        self.client.logout()
        response = self.client.get('/page_details/1/')
        self.assertRedirects(response, expected_url='/accounts/login/', status_code=302, target_status_code=200)

    def test_page_details_without_page_id(self):
        """
        If site_id is not given,
        user should see an error page.
        """
        response = self.client.get('/page_details/')
        self.assertTemplateUsed(response, template_name='register_site/error_page.html')

    def test_page_details_with_id_of_non_existing_site(self):
        """
        If page with given site_id don't exists,
        user should see an error page.
        """
        response = self.client.get('/page_details/99/')
        self.assertTemplateUsed(response, template_name='register_site/error_page.html')

    def test_page_details_with_correct_page_id(self):
        """
        If site_id is correct,
        user should see page with data about given entry.
        """
        response = self.client.get('/page_details/1/')
        self.assertTemplateUsed(response, template_name='manage_sites/site_details.html')


class EditPageTests(TestCase):

    def setUp(self):
        # Set up a user
        user = User.objects.create_user("test", 'random@rand.eu', "abc123de")
        user.save()
        self.client.login(username='test', password='abc123de')
        # Add site to DB for testing purposes
        site_index = SitesIndex(
            id=1,
            alias="Test site",
            owner_username="test",
            url="test.com",
            page=1
        )
        site_index.save()
        site_data = RegisterSite(
            alias=site_index.alias,
            site_id=site_index.id,
            url=site_index.url,
            title="test title",
            description="test description",
            h1="test h1",
            timestamp="now",
            updated="now"
        )
        site_data.save()
        site_scanner = ScannerEngineSite(
            site_id=site_index.id,
            url=site_index.url,
            status_code=200,
            title=site_data.title,
            description=site_data.description,
            h1=site_data.h1,
            timestamp=site_data.timestamp
        )
        site_scanner.save()

    def test_edit_without_page_id(self):
        """
        If site_id is not given,
        user should see an error page.
        """
        response = self.client.get('/modify_site/')
        self.assertTemplateUsed(response, template_name='register_site/error_page.html')

    def test_edit_with_unregistered_user(self):
        """
        If user is unauthenticated,
        redirect to the login page.
        """
        self.client.logout()
        response = self.client.get('/modify_site/1/')
        self.assertRedirects(response, expected_url='/accounts/login/', status_code=302, target_status_code=200)

    def test_edit_with_id_of_non_existing_site(self):
        """
        If page with given site_id don't exists,
        user should see an error page.
        """
        response = self.client.get('/modify_site/99/')
        self.assertTemplateUsed(response, template_name='register_site/error_page.html')

    def test_edit_with_correct_page_id_and_new_value(self):
        """
        If site_id is correct and attribute-value pair was given,
        modify site in the DB.
        """
        self.client.post('/modify_site/1/', {
            'attribute': 'title',
            'value': 'new title'
        })
        entry_from_db = RegisterSite.objects.get(site_id=1)
        self.assertEqual(entry_from_db.title, 'new title')

    def test_edit_with_correct_page_id_and_empty_string_value(self):
        """
        If site_id is correct and new value is empty string,
        modify site in the DB.
        """
        self.client.post('/modify_site/1/', {
            'attribute': 'title',
            'value': ''
        })
        entry_from_db = RegisterSite.objects.get(site_id=1)
        self.assertEqual(entry_from_db.title, '')

    def test_edit_without_new_value(self):
        """
        If attribute-value par was not given,
        show error message to the user.
        """
        self.client.post('/modify_site/1/', {})
        entry_from_db = RegisterSite.objects.get(site_id=1)
        # Value in db should not be changed.
        self.assertEqual(entry_from_db.title, 'test title')

    def test_edit_with_next_url_parameter(self):
        """
        If next_url was send with post,
        redirect user to next_url after finished
        """
        response = self.client.post('/modify_site/1/', {
            'attribute': 'title',
            'value': 'new value',
            'next_url': 'page_details/1/'
        })
        entry_from_db = RegisterSite.objects.get(site_id=1)
        self.assertEqual(entry_from_db.title, 'new value')
        self.assertRedirects(response, expected_url='/page_details/1/', status_code=302, target_status_code=200)
