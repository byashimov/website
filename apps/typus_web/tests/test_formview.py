import unittest

from flask_testing import TestCase

from flask import current_app, url_for

from http import HTTPStatus
from website import site


class FormViewTestCase(TestCase):
    def setUp(self):
        self.client = site.test_client()
        with site.app_context():
            self.url = url_for('typus_web.form_view')

    def create_app(self):
        return site

    def test_get_ok(self):
        response = self.client.get(self.url)
        self.assert200(response)

    def test_invalid_form(self):
        response = self.client.post(self.url, data={})
        self.assertStatus(response, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_valid_form(self):
        response = self.client.post(self.url, data={'text': '"test"'})
        self.assert200(response)

        form = self.get_context_variable('form')
        self.assertEqual(form.text.data, '“test”')

    def test_escape_phrases(self):
        data = {
            'text': '"test" (c) (r) (tm)',
            'escape_phrases': '(c), (r)'
        }
        response = self.client.post(self.url, data=data)
        form = self.get_context_variable('form')
        self.assertEqual(form.text.data, '“test” (c) (r)™')

    def test_diff_is_none(self):
        response = self.client.post(self.url, data={'text': 'test'})
        self.assert200(response)
        self.assertContext('diff', None)

    def test_diff(self):
        response = self.client.post(self.url, data={'text': '"test"'})
        self.assert200(response)
        self.assertContext('diff', '<mark>“</mark>test<mark>”</mark>')

    def test_diff_with_escaped_html(self):
        response = self.client.post(self.url, data={'text': '"<b>test</b>"'})
        self.assert200(response)
        self.assertContext(
            'diff', '<mark>“</mark>&lt;b&gt;test&lt;/b&gt;<mark>”</mark>')

    def test_ru_typus(self):
        url = self.url + '?lang=ru'
        response = self.client.post(url, data={'text': '"тест"'})
        self.assert200(response)

        form = self.get_context_variable('form')
        self.assertEqual(form.text.data, '«тест»')
