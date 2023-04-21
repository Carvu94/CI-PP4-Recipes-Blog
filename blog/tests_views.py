from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from .models import (
    Cookbook,
    Comment,
    Recipe,
    Category,
    Profile
)
from .views import RecipeDetail, CommentForm, EditComment


class HomeViewTest(TestCase):
    """
    home view test
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('home')
        mixer.cycle(3).blend(Recipe, status=1, likes=mixer.RANDOM)
        mixer.cycle(2).blend(Recipe, status=0, likes=mixer.RANDOM)

    def test_home_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_view_queryset(self):
        response = self.client.get(self.url)
        recipes = response.context['object_list']
        self.assertEqual(recipes.count(), 3)
        for recipe in recipes:
            self.assertEqual(recipe.status, 1)
        self.assertEqual(list(recipes),
                         list(
            Recipe.objects.filter(status=1).order_by('likes')[:3]))


class TestSearchResultsView(TestCase):
    """
    test search results view
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_results')

    def test_search_results_view_with_post_request(self):
        recipe = Recipe.objects.create(
            title='Recipe',
            content='Recipe',
            time_to_cook=1
        )
        searched = 'Recipe'
        response = self.client.post(self.url, {'searched': searched})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        self.assertIn(searched, str(response.content))
        self.assertIn(recipe.title, str(response.content))

    def test_search_results_view_with_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        self.assertNotIn('searched', str(response.content))
        self.assertNotIn('recipe', str(response.content))


class CategoriesListViewTest(TestCase):
    """
    test categories list view
    """
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title='Category 1')
        Category.objects.create(title='Category 2')
        Category.objects.create(title='Category 3')

    def test_view_url_exists(self):
        response = self.client.get('/categories_recipes/<str:cats>')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')

    def test_queryset(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
        self.assertQuerysetEqual(
            response.context['object_list'],
            ['<Category: Category 1>',
             '<Category: Category 2>',
             '<Category: Category 3>'],
            ordered=False
        )


class CategoriesViewTest(TestCase):
    """
    test categories view
    """
    def setUp(self):
        self.client = Client()
        self.category1 = Category.objects.create(title='Category1')
        self.recipe1 = Recipe.objects.create(
            title='Recipe1',
            content='Recipe1 content')
        self.recipe1.categories.add(self.category1)

    def test_categories_view(self):
        url = reverse('categories', args=['category1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories_recipes.html')
        self.assertContains(response, 'Recipe1')
        self.assertEqual(response.context['cats'], 'Category1')
        self.assertQuerysetEqual(response.context['categories_recipes'],
                                 ['<Recipe: Recipe1>'])


class CookbookListTest(TestCase):
    """
    test cookbook list view
    """
    @classmethod
    def setUpTestData(cls):
        # Create 10 cookbooks for testing
        number_of_cookbooks = 10
        for cookbook_id in range(number_of_cookbooks):
            Cookbook.objects.create(
                author=User.objects.create_user(
                    username=f'testuser{cookbook_id}'),
                title=f'Test Cookbook {cookbook_id}',
                content=f'Test content {cookbook_id}',
                approved=True,
                status=1
            )

    def test_view_url_exists(self):
        response = self.client.get('/cookbooks/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cookbooks'))
        self.assertEqual(response.status_code, 200)

    def test__correct_template(self):
        response = self.client.get(reverse('cookbooks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cookbooks.html')

    def test_pagination(self):
        response = self.client.get(reverse('cookbooks'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['cookbook_list']) == 6)

    def test_lists_all_cookbooks(self):
        # Get second page and confirm it has remaining (4) items
        response = self.client.get(reverse('cookbooks')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['cookbook_list']) == 4)


class CookbookDetailViewTest(TestCase):
    """
    test cookbook detail vew
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass')
        self.cookbook = Cookbook.objects.create(
            author=self.user, title='Test Cookbook', content='Test content')
        self.recipe1 = Recipe.objects.create(
            title='Test Recipe 1', content='Test content', author=self.user)
        self.recipe2 = Recipe.objects.create(
            title='Test Recipe 2', content='Test content', author=self.user)
        self.cookbook.recipes.add(self.recipe1)
        self.cookbook.recipes.add(self.recipe2)
        self.url = reverse('cookbook_detail', args=[self.cookbook.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cookbook_detail.html')
        self.assertEqual(response.context['cookbook'], self.cookbook)
        self.assertQuerysetEqual(
            response.context['recipes'],
            [repr(self.recipe1), repr(self.recipe2)],
            ordered=False
        )
        self.assertFalse(response.context['liked'])

    def test_get_liked(self):
        self.client.login(username='testuser', password='testpass')
        self.cookbook.likes.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['liked'])


class CookbookLikeViewTestCase(TestCase):
    """
    Test cookbook like view
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.cookbook = Cookbook.objects.create(
            author=self.user,
            title='test',
            content='test',
            approved=True
        )
        self.url = reverse('cookbook_like', args=[self.cookbook.id])

    def test_like_unauthenticated_user(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_like_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'cookbook_detail', args=[self.cookbook.id]))
        self.cookbook.refresh_from_db()
        self.assertIn(self.user, self.cookbook.likes.all())

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'cookbook_detail', args=[self.cookbook.id]))
        self.cookbook.refresh_from_db()
        self.assertNotIn(self.user, self.cookbook.likes.all())


class AddCookbookViewTestCase(TestCase):
    """
    test add cookbook view
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('add_cookbook')
        self.user = User.objects.create_user(
            username='testuser',
            password='12345')

    def test_add_cookbook_view_with_valid_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {
            'title': 'test',
            'content': 'test',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cookbook.objects.count(), 1)
        cookbook = Cookbook.objects.first()
        self.assertEqual(cookbook.title, 'test')
        self.assertEqual(cookbook.content, 'test')
        self.assertEqual(cookbook.author, self.user)

    def test_add_cookbook_view_with_invalid_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {
            'title': '',
            'content': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_cookbook.html')
        self.assertContains(response, 'Sorry, the cookbook was not created')
        self.assertEqual(Cookbook.objects.count(), 0)


class EditCookbookViewTest(TestCase):
    """
    test edit cookbook view
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.cookbook = Cookbook.objects.create(
            title='test', content='test', author=self.user
        )

    def test_edit_cookbook_view(self):
        # Login the user
        self.client.login(username='testuser', password='12345')

        # Make a POST request to the EditCookbookView with updated data
        response = self.client.post(
            reverse('edit_cookbook', kwargs={'pk': self.cookbook.pk}),
            data={
                'title': 'Updated Title',
                'content': 'Updated Content',
                'recipes': [],
            },
        )

        # Check that the update is successful
        self.assertEqual(response.status_code, 302)
        self.cookbook.refresh_from_db()
        self.assertEqual(self.cookbook.title, 'Updated Title')
        self.assertEqual(self.cookbook.content, 'Updated Content')


class DeleteCookbookViewTestCase(TestCase):
    """
    test delete cookbook view
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.cookbook = Cookbook.objects.create(
            title='test', content='test', author=self.user)

    def test_delete_cookbook(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('delete_cookbook', args=[self.cookbook.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cookbooks'))
        self.assertFalse(Cookbook.objects.filter(id=self.cookbook.id).exists())


class RecipeListViewTest(TestCase):
    """
    Test recipe list view
    """
    @classmethod
    def setUpTestData(self):
        # Set up objects used by all test methods
        for i in range(10):
            Recipe.objects.create(
                title=f"Recipe {i}",
                content=f"Content for recipe {i}",
                author_id=1,
                status=1
            )
        self.url = reverse('recipes')

    def setUp(self):
        self.client = Client()

    def test_recipe_list_view_url_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'recipes.html')

    def test_recipe_list_view_pagination(self):
        response = self.client.get(self.url)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['recipe_list']) == 6)

    def test_recipe_list_view_context(self):
        response = self.client.get(self.url)
        self.assertTrue('recipe_list' in response.context)
        self.assertTrue(isinstance(response.context['recipe_list'], list))
        self.assertTrue(len(response.context['recipe_list']) == 6)

    def test_recipe_list_view_all_recipes_displayed(self):
        response = self.client.get(self.url)
        self.assertTrue(len(response.context['recipe_list']) == 6)
        response = self.client.get(self.url+'?page=2')
        self.assertTrue(len(response.context['recipe_list']) == 4)


class AddRecipeViewTest(TestCase):
    """
    test add recipe view
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_add_recipe(self):
        response = self.client.post(
            reverse('add_recipe'),
            {
                'title': 'Test Recipe',
                'content': 'This is a test recipe.',
                'categories': 'Test Category',
                'time_to_cook': '30 minutes'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.first().title, 'Test Recipe')


class AddRecipeViewTest(TestCase):
    """
    test add recipe view
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('add_recipe')

    def test_add_recipe_view(self):
        data = {
            'title': 'test',
            'content': 'test',
            'categories': 'test',
            'time_to_cook': '1'
        }
        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recipe.objects.filter(title='Test Recipe').exists())
        recipe = Recipe.objects.get(title='Test Recipe')
        self.assertEqual(recipe.status, Recipe.WAITING_APPROVAL)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Recipe added successfully,'
                         'and It is waiting for approval.')


class EditRecipeViewTest(TestCase):
    """
    test edit recipe view
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.recipe = Recipe.objects.create(
            title='test',
            content='test',
            author=self.user,
            time_to_cook=3
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_edit_recipe(self):
        url = reverse('edit_recipe', kwargs={'pk': self.recipe.pk})
        data = {
            'title': 'Updated test',
            'content': 'Updated test',
            'categories': 'Updated test',
            'time_to_cook': 1
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Updated test')
        self.assertEqual(self.recipe.content, 'Updated test')
        self.assertEqual(self.recipe.categories, 'Updated test')
        self.assertEqual(self.recipe.time_to_cook, 1)


class DeleteRecipeViewTest(TestCase):
    """
    Test delete recipe view
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            title='test', content='test', author=self.user)

    def test_delete_recipe(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_recipe',
                                            args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes'))
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())
        self.assertContains(response, 'Recipe deleted successfully!')


class RecipeDetailViewTest(TestCase):
    """
    test recipe detail view
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.view = RecipeDetail.as_view()
        self.recipe = mixer.blend(Recipe, status=1)

    def test_get_recipe_detail(self):
        url = reverse('recipe-detail', kwargs={'slug': self.recipe.slug})
        request = self.factory.get(url)
        response = self.view(request, slug=self.recipe.slug)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
        self.assertEqual(response.context_data['recipe'], self.recipe)
        self.assertFalse(response.context_data['commented'])
        self.assertFalse(response.context_data['liked'])
        self.assertIsInstance(response.context_data['comment_form'],
                              CommentForm)

    def test_post_valid_comment(self):
        url = reverse('recipe-detail', kwargs={'slug': self.recipe.slug})
        request = self.factory.post(url, data={'body': 'Test comment'})
        request.user = mixer.blend('auth.User')
        response = self.view(request, slug=self.recipe.slug)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
        self.assertEqual(response.context_data['recipe'], self.recipe)
        self.assertTrue(response.context_data['commented'])
        self.assertFalse(response.context_data['liked'])
        self.assertIsInstance(response.context_data['comment_form'],
                              CommentForm)
        self.assertEqual(response.context_data['comments'].count(), 1)
        self.assertEqual(response.context_data['comments'][0].body,
                         'Test comment')
        self.assertEqual(response.context['messages']._queued_messages[0].tags,
                         'success')

    def test_post_invalid_comment(self):
        url = reverse('recipe-detail', kwargs={'slug': self.recipe.slug})
        request = self.factory.post(url, data={'body': ''})
        request.user = mixer.blend('auth.User')
        response = self.view(request, slug=self.recipe.slug)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
        self.assertEqual(response.context_data['recipe'], self.recipe)
        self.assertFalse(response.context_data['commented'])
        self.assertFalse(response.context_data['liked'])
        self.assertIsInstance(response.context_data['comment_form'],
                              CommentForm)
        self.assertEqual(response.context['messages']._queued_messages[0].tags,
                         'error')


class DeleteCommentViewTest(TestCase):
    """
    test delete comment view
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.recipe = Recipe.objects.create(
            title='test',
            slug='test',
            body='test',
            author=self.user,
        )
        self.comment = Comment.objects.create(
            name='test User',
            body='test',
            post=self.recipe,
        )

    def test_delete_comment(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_comment',
                                            args=[self.comment.id]))
        self.assertRedirects(response, reverse('recipe_detail',
                                               args=[self.recipe.slug]))
        self.assertEqual(Comment.objects.count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'The comment was deleted successfully')

    def test_delete_comment_unauthenticated(self):
        response = self.client.post(reverse('delete_comment',
                                            args=[self.comment.id]))
        self.assertRedirects(response,
                             reverse('login') + '?next=' +
                             reverse('delete_comment', args=[self.comment.id]))
        self.assertEqual(Comment.objects.count(), 1)


class EditCommentTest(TestCase):
    """
    test edit comment view
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = mixer.blend(User)
        self.recipe = mixer.blend(Recipe)
        self.comment = mixer.blend(Comment, post=self.recipe, author=self.user)

    def test_get(self):
        url = reverse('edit_comment', args=[self.comment.pk])
        request = self.factory.get(url)
        request.user = self.user
        response = EditComment.as_view()(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_comment.html')
        self.assertEqual(response.context_data['comment'], self.comment)

    def test_post_valid_form(self):
        url = reverse('edit_comment', args=[self.comment.pk])
        data = {'body': 'New comment body'}
        request = self.factory.post(url, data=data)
        request.user = self.user
        response = EditComment.as_view()(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipe_detail',
                                               args=[self.recipe.slug]))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, data['body'])

    def test_post_invalid_form(self):
        url = reverse('edit_comment', args=[self.comment.pk])
        data = {'body': ''}
        request = self.factory.post(url, data=data)
        request.user = self.user
        response = EditComment.as_view()(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_comment.html')
        self.assertIn('form', response.context_data)
        self.assertFalse(response.context_data['form'].is_valid())
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.body, data['body'])


class RecipeLikeTest(TestCase):
    """
    test recipe like view
    """
    def setUp(self):
        self.client = Client()
        self.user = mixer.blend(User)
        self.recipe = mixer.blend(Recipe)

    def test_recipe_like(self):
        self.client.force_login(self.user)
        url = reverse('recipe_like', args=[self.recipe.slug])
        response = self.client.post(url)
        self.assertRedirects(
            response, reverse('recipe_detail', args=[self.recipe.slug])
        )
        self.recipe.refresh_from_db()
        self.assertIn(self.user, self.recipe.likes.all())
        response = self.client.post(url)
        self.assertRedirects(
            response, reverse('recipe_detail', args=[self.recipe.slug])
        )
        self.recipe.refresh_from_db()
        self.assertNotIn(self.user, self.recipe.likes.all())


class ProfilePageViewTest(TestCase):
    """
    test profile page view
    """
    def setUp(self):
        self.user_profile = Profile.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User'
        )

    def test_profile_page_view(self):
        url = reverse('profile', kwargs={'pk': self.user_profile.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')
        self.assertContains(response, self.user_profile.username)
        self.assertContains(response, self.user_profile.first_name)
        self.assertContains(response, self.user_profile.last_name)


class EditProfilePageViewTest(TestCase):
    """
    test edit profile page view
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio='test bio')

    def test_edit_profile_page_view_success(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('edit_profile',
                                            args=[self.profile.id]), {
            'bio': 'new test bio',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.get(id=self.profile.id).bio,
                         'new test bio')

    def test_edit_profile_page_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('edit_profile',
                                           args=[self.profile.id]))
        self.assertRedirects(response,
                             '/accounts/login/?next=/profile/edit/%d/' %
                             self.profile.id)


class DeleteUserProfileTestCase(TestCase):
    """
    test delete user profile view
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user, bio='test'
        )

    def test_delete_profile(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_profile',
                                            args=[self.profile.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.client.logout()
