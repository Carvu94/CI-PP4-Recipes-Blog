from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    Cookbook,
    Comment,
    Recipe,
    Category,
    Profile
)


class CategoryModelTest(TestCase):
    """
    Test category model
    """
    @classmethod
    def setUpTestData(self):
        Category.objects.create(title='Test')

    def test_title_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_title(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'{category.title}'
        self.assertEquals(expected_object_name, str(category))


class RecipeModelTest(TestCase):
    """
    Test Recipe model
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.category = Category.objects.create(title='Test Category')
        self.recipe = Recipe.objects.create(
            title='Test',
            author=self.user,
            content='Test',
            excerpt='Test',
            status=1,
            time_to_cook=30,
        )
        self.recipe.categories.add(self.category)

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Test')

    def test_recipe_slug(self):
        self.assertEqual(self.recipe.slug, 'test')

    def test_recipe_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), '/recipes/')

    def test_recipe_number_of_likes(self):
        self.assertEqual(self.recipe.number_of_likes(), 0)

    def test_recipe_categories(self):
        self.assertEqual(self.recipe.categories.first().title, 'Test')


class CommentModelTest(TestCase):
    """
    Test comment model
    """
    def setUp(self):
        self.recipe = Recipe.objects.create(
            title='test',
            content='test',
            slug='test'
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            post=self.recipe,
            name='test',
            body='test'
        )
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(
            comment.__str__(),
            f"Comment {comment.body} by {comment.name}")
        self.assertEqual(comment.post, self.recipe)


class ProfileModelTest(TestCase):
    """
    Test profile model
    """
    @classmethod
    def setUpTestData(self):
        testuser = User.objects.create_user(
            username='test', password='test')
        Profile.objects.create(user=testuser, bio='test')

    def test_profile_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_profile_bio_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')

    def test_profile_image_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_profile_str(self):
        profile = Profile.objects.get(id=1)
        expected_str = str(profile.user)
        self.assertEqual(str(profile), expected_str)

    def test_profile_get_absolute_url(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.get_absolute_url(), '/home')


class CookbookModelTestCase(TestCase):
    """
    Test cookbook model
    """
    @classmethod
    def setUpTestData(self):
        # Test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.user.save()

        # Create two test recipes
        self.recipe1 = Recipe.objects.create(
            title='Recipe 1',
            author=self.user,
            content='This is the content of Recipe 1',
            excerpt='Excerpt of Recipe 1',
            time_to_cook=30,
        )
        self.recipe2 = Recipe.objects.create(
            title='Recipe 2',
            author=self.user,
            content='This is the content of Recipe 2',
            excerpt='Excerpt of Recipe 2',
            time_to_cook=60,
        )

    def test_cookbook_creation(self):
        cookbook = Cookbook.objects.create(
            author=self.user,
            title='test',
            content='test',
            featured_image='http://test.com/mycookbook.jpg',
            approved=True,
            status=1,
        )

        cookbook.recipes.add(self.recipe1)
        cookbook.recipes.add(self.recipe2)

        self.assertEqual(cookbook.title, 'test')
        self.assertEqual(cookbook.content, 'test')
        self.assertEqual(cookbook.author, self.user)
        self.assertEqual(
            cookbook.featured_image,
            'http://test.com/mycookbook.jpg'
            )
        self.assertEqual(cookbook.approved, True)
        self.assertEqual(cookbook.status, 1)
        self.assertEqual(cookbook.number_of_likes(), 0)
        self.assertEqual(cookbook.recipes.count(), 2)

    def test_cookbook_str_method(self):
        cookbook = Cookbook.objects.create(
            author=self.user,
            title='test',
            content='test',
            featured_image='http://test.com/mycookbook.jpg',
            approved=True,
            status=1,
        )

        self.assertEqual(str(cookbook), 'test')
