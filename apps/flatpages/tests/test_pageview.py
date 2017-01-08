from flask_testing import TestCase

from flask import url_for

from website import site


class IndexPageTestCase(TestCase):
    def setUp(self):
        self.client = site.test_client()
        with site.app_context():
            self.url = url_for('flatpages.index')

    def create_app(self):
        return site

    def test_index(self):
        response = self.client.get(self.url)
        self.assert200(response)

    def test_method_not_allowed(self):
        response = self.client.post(self.url)
        self.assert405(response)
