from flask_testing import TestCase

from flask import url_for

from website import site


class PageTestMixin:
    endpoint = NotImplemented
    endpoint_options = {}

    def setUp(self):
        self.client = site.test_client()
        with site.app_context():
            self.url = url_for(self.endpoint, **self.endpoint_options)

    def create_app(self):
        return site

    def test_index(self):
        response = self.client.get(self.url)
        self.assert200(response)

    def test_method_not_allowed(self):
        response = self.client.post(self.url)
        self.assert405(response)


class IndexPageTestCase(TestCase):
    endpoint = 'flatpages.index_view'


class TypusApiPageTestCase(TestCase):
    endpoint = 'flatpages.page_view'
    endpoint_options = {'path': 'typus/api'}
