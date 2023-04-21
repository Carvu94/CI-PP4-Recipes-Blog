from django.test import TestCase
from blog.forms import AddCookbookForm


class TestAddCookbookForm(TestCase):
    """
    Test add book form
    """
    def test_form_fields(self):
        form = AddCookbookForm()
        expected_fields = ['title', 'content', 'recipes', 'featured_image']
        self.assertSequenceEqual(expected_fields, list(form.fields.keys()))

    def test_form_valid_data(self):
        form_data = {
            'title': 'Test',
            'content': 'Test',
            'featured_image': 'test.jpg',
        }
        form = AddCookbookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'title': '',
            'content': 'test',
            'featured_image': 'test.jpg'
        },
        form = AddCookbookForm(data=form_data)
        self.assertFalse(form.is_valid())
