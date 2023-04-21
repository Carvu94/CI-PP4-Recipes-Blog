from django.test import TestCase
from .forms import (
    AddCookbookForm,
    EditCookbookForm,
    CommentForm,
    ProfilePageForm,
    EditRecipe
)
from .models import Cookbook, Comment, Recipe


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


class EditCookbookFormTest(TestCase):
    """
    Test edit book form
    """    
    def test_form_valid(self):
        coobook = Cookbook.objects.create(
            title='Test',
            content='Test',
            featured_image='test.jpg',
            )
        data = {
            'title': 'test',
            'content': 'test',
            'recipes': None,
            'featured_image': 'test2.jpg'
            }
        form = EditCookbookForm(data=data, instance=coobook)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        cookbook = Cookbook.objects.create(
            title='test',
            content='test',
            featured_image='noturl'
            )
        data = {
            'title': '',
            'content': '',
            'recipes': None,
            'featured_image':
            'test2.jpg'
            }
        form = EditCookbookForm(data=data, instance=cookbook)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    """
    Test comment form
    """    
    def test_form_valid_data(self):
        form = CommentForm(data={'body': 'This is a test comment.'})
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertIsNone(comment.pk)

    def test_form_blank_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'body': ['This field is required.']})


class ProfilePageFormTestCase(TestCase):
    """
    Test profile page form
    """
    def test_valid_form(self):
        form_data = {
            'bio': 'test',
        }
        form = ProfilePageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'bio': '',
        }
        form = ProfilePageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('bio', form.errors)


