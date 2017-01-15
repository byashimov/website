from flask_testing import TestCase

from flask import url_for

from http import HTTPStatus
from website import site


class ApiViewTestCase(TestCase):
    def setUp(self):
        self.client = site.test_client()
        with site.app_context():
            self.url = url_for('typus_web.api_view')

    def create_app(self):
        return site

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assert405(response)

    def test_post_invalid(self):
        response = self.client.post(self.url, data={})
        self.assertStatus(response, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.json)

    def test_post_valid(self):
        data = {'text': '"test"', 'lang': 'en'}
        response = self.client.post(self.url, data=data)
        self.assert200(response)
        self.assertEqual(response.json, {'text': '“test”'})

    def test_post_escape_phrases(self):
        data = {
            'text': '"test" (c) (r) (tm)',
            'escape_phrases': '(c), (r)'
        }
        response = self.client.post(self.url, data=data)
        self.assert200(response)
        self.assertEqual(response.json, {'text': '“test” (c) (r)™'})

    def test_post_lang_ru(self):
        data = {'text': '"тест"', 'lang': 'ru'}
        response = self.client.post(self.url, data=data)
        self.assert200(response)
        self.assertEqual(response.json, {'text': '«тест»'})
