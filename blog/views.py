from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from .models import Recipe, Category, Comment, Profile, Cookbook
from .forms import (
    CommentForm,
    ProfilePageForm,
    AddCookbookForm,
    EditRecipe,
    EditCookbookForm
    )
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class HomeView(generic.ListView):
    """
    Renders the Home page
    """
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('likes')[:3]
    template_name = 'index.html'


def about(request):
    """
    Renders About page
    """
    return render(request, "about.html")


def contact_us(request):
    """
    Renders contact us page
    """
    return render(request, "contact.html")


def search_results(request):
    """
    Search Recipes
    """
    if request.method == "POST":
        searched = request.POST['searched']
        recipes = Recipe.objects.filter(
            title__icontains=searched)

        return render(request, 'search_results.html',
                      {'searched': searched, 'recipes': recipes})
    else:
        return render(request, 'search_results.html', {})


class CategoriesList(generic.ListView):
    """
    Renders Categories page
    """
    model = Category
    template_name = 'categories.html'


def categories_view(request, cats):
    """
    Renders the posts filtered by categories
    """
    categories_recipes = Recipe.objects.filter(
        categories__title__contains=cats)
    return render(request, 'categories_recipes.html', {
        'cats': cats.title(), 'categories_recipes': categories_recipes})


class CookbookList(generic.ListView):
    """
    Renders the cookbook page
    """
    model = Cookbook
    queryset = Cookbook.objects.filter(status=1).order_by('-created_on')
    template_name = 'cookbooks.html'
    paginate_by = 6


class CookbookDetail(View):
    """
    Renders the cookbook detail page
    """
    def get(self, request, id, *args, **kwargs):
        cookbook = Cookbook.objects.get(id=id)
        recipes = cookbook.recipes.all()
        liked = False
        if cookbook.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "cookbook_detail.html",
            {
                "cookbook": cookbook,
                "recipes": recipes,
                "liked": liked,
            },
        )

    def post(self, request, id, *args, **kwargs):
        cookbook = Cookbook.objects.get(id=id)
        recipes = cookbook.recipes.all()
        liked = False
        if cookbook.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "cookbook_detail.html",
            {
                "cookbook": cookbook,
                "recipes": recipes,
                "liked": liked,
            },
        )


class CookbookLike(LoginRequiredMixin, View):
    """
    Like Cookbook
    """
    def post(self, request, id, *args, **kwargs):
        book = get_object_or_404(Cookbook, id=id)

        if book.likes.filter(id=request.user.id).exists():
            book.likes.remove(request.user)
        else:
            book.likes.add(request.user)

        return HttpResponseRedirect(reverse('cookbook_detail', args=[id]))


class AddCookbookView(generic.CreateView):
    model = Cookbook
    template_name = 'add_cookbook.html'
    fields = (
        'title',
        'content',
        'featured_image'
        )

    def upload(request):
        context = dict(backend_form=AddCookbookForm())

        if request.method == 'POST':
            form = AddCookbookForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()

        return render(request, 'add_cookbook.html', context)

    def post(self, request, *args, **kwargs):
        form = AddCookbookForm(data=request.POST)
        if form.is_valid():
            cookbook = form.save(commit=False)
            cookbook.author = request.user
            cookbook.save()
            messages.success(self.request,
                             'Your cookbook is created,'
                             'and it is waiting approval')
            form.save_m2m()
            return redirect(cookbook.get_absolute_url())
        else:
            messages.warning(self.request,
                             'Sorry, the cookbook was not created,'
                             'please try again.')
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class EditCookbookView(LoginRequiredMixin, UpdateView):
    """
    Edit Cookbook
    """
    model = Cookbook
    template_name = 'edit_cookbook.html'
    fields = (
        'title',
        'content',
        'recipes',
        'featured_image'
        )

    def upload(request):
        context = dict(backend_form=EditCookbookForm())

        if request.method == 'POST':
            form = EditCookbookForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()

        return render(request, 'edit_cookbook.html', context)

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Cookbook edited successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,
                       'Error editing cookbook.'
                       'Please check the form and try again.')
        return response


@method_decorator(login_required, name='dispatch')
class DeleteCookbookView(DeleteView):
    """
    Delete Cookbook
    """
    model = Cookbook
    template_name = 'delete_cookbook.html'
    success_url = reverse_lazy('cookbooks')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Cookbook deleted successfully!')

        return response


class RecipeList(generic.ListView):
    """
    Renders the recipes page
    """
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'recipes.html'
    paginate_by = 8


@method_decorator(login_required, name='dispatch')
class AddRecipeView(generic.CreateView):
    model = Recipe
    template_name = 'add_recipe.html'
    fields = (
        'title',
        'content',
        'featured_image',
        'categories',
        'time_to_cook')

    def upload(request):
        context = dict(backend_form=EditRecipe())

        if request.method == 'POST':
            form = EditRecipe(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()

        return render(request, 'edit_recipe.html', context)

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
                         'Recipe added successfully,'
                         'and It is waiting for approval.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,
                       'Error adding recipe.'
                       'Please check the form and try again.')
        return response


@method_decorator(login_required, name='dispatch')
class EditRecipeView(LoginRequiredMixin, UpdateView):
    """
    Edit Recipe
    """
    model = Recipe
    template_name = 'edit_recipe.html'
    fields = (
        'title',
        'content',
        'categories',
        'time_to_cook',
        'featured_image'
        )

    def upload(request):
        context = dict(backend_form=EditRecipe())

        if request.method == 'POST':
            form = EditRecipe(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()

        return render(request, 'edit_recipe.html', context)

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
                         'Recipe edited successfully.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,
                       'Error editing recipe.'
                       'Please check the form and try again.')
        return response


@method_decorator(login_required, name='dispatch')
class DeleteRecipeView(DeleteView):
    """
    Delete Recipe
    """
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('recipes')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Recipe deleted successfully!')

        return response


class RecipeDetail(View):
    """
    Renders the recipe detail page
    """
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = recipe
            comment.save()
            messages.success(request,
                             'The comment was posted,'
                             'and it is waiting approval.')
        else:
            comment_form = CommentForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


@login_required
def delete_comment(request, comment_id):
    """
    Delete comment
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'The comment was deleted successfully')

    return HttpResponseRedirect(reverse(
        'recipe_detail', args=[comment.post.slug]
    ))


@method_decorator(login_required, name='dispatch')
class EditComment(LoginRequiredMixin, UpdateView):
    """
    Edit Comment
    """
    model = Comment
    template_name = 'edit_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
                         'Comment edited successfully.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,
                       'Error editing comment.'
                       'Please check the form and try again.')
        return response


class RecipeLike(LoginRequiredMixin, View):
    """
    Like Recipe
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Recipe, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            messages.success(request, 'You have unliked this post.')
        else:
            post.likes.add(request.user)
            messages.success(request, 'You have liked this post.')

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class ProfilePageView(DetailView):
    """
    Profile Page Veiw
    """
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfilePageView, self).get_context_data(
            *args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context


class CreateProfileView(LoginRequiredMixin, CreateView):
    """
    Create User Profile
    """
    model = Profile
    form_class = ProfilePageForm
    template_name = 'create_profile.html'

    def upload(request):
        context = dict(backend_form=EditRecipe())

        if request.method == 'POST':
            form = ProfilePageForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()

        return render(request, 'home', context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
                         'Profile created successfully.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,
                       'Error creating a profile.'
                       'Please check the form and try again.')
        return response


@method_decorator(login_required, name='dispatch')
class EditProfilePageView(LoginRequiredMixin, UpdateView):
    """
    Edit User Profile
    """
    model = Profile
    template_name = 'edit_profile.html'
    fields = ('user', 'bio', 'image')
    success_url = reverse_lazy('home')

    def upload(request):
        context = dict(backend_form=ProfilePageForm())

        if request.method == 'POST':
            form = ProfilePageForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()
        return render(request, 'user_profile.html', context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,
                         'Profile edited successfully.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,
                       'Error editing a profile.'
                       'Please check the form and try again.')
        return response


@method_decorator(login_required, name='dispatch')
class DeleteUserProfile(LoginRequiredMixin, DeleteView):
    """
    Delete User Profile
    """
    model = Profile
    template_name = 'delete_profile.html'
    form_class = ProfilePageForm
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        messages.success(request, 'The profile was deleted successfully')

        return HttpResponseRedirect(reverse('home'))
