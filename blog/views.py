from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from .models import Recipe, Category, Comment, Profile, Cookbook
from .forms import CommentForm, ProfilePageForm, AddCookbookForm
from django.http import HttpResponseRedirect
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

    # def get_context_data(self, *args, **kwargs):
    #     cat_menu = Category.objects.all()
    #     context = super(HomeView, self).get_context_data(*args, **kwargs)
    #     context["cat_menu"] = cat_menu
    #     return context


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
        # queryset = Cookbook.objects.filter(status=1)
        # cookbook = get_object_or_404(queryset, id=id)
        # comments = cookbook.cookbooks.filter(approved=True).order_by(
        #     'created_on')
        liked = False
        if cookbook.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "cookbook_detail.html",
            {
                "cookbook": cookbook,
                "recipes": recipes,
                # "comments": comments,
                # "commented": False,
                "liked": liked,
                # "comment_form": BookCommentForm()
            },
        )

    def post(self, request, id, *args, **kwargs):
        cookbook = Cookbook.objects.get(id=id)
        recipes = cookbook.recipes.all()
        # queryset = Cookbook.objects.filter(status=1)
        # cookbook = get_object_or_404(queryset, id=id)
        # comments = cookbook.cookbooks.filter(approved=True).order_by(
        #     'created_on')
        liked = False
        if cookbook.likes.filter(id=self.request.user.id).exists():
            liked = True

        # comment_form = BookCommentForm(data=request.POST)

        # if comment_form.is_valid():
        #     comment_form.instance.email = request.user.email
        #     comment_form.instance.name = request.user.username
        #     comment = comment_form.save(commit=False)
        #     comment.cookbook = cookbook
        #     comment.save()
        # else:
        #     comment_form = BookCommentForm()

        return render(
            request,
            "cookbook_detail.html",
            {
                "cookbook": cookbook,
                "recipes": recipes,
                # "comments": comments,
                # "commented": True,
                "liked": liked,
                # "comment_form": BookCommentForm()
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
        'content')

    def post(self, request, *args, **kwargs):
        form = AddCookbookForm(data=request.POST)
        if form.is_valid():
            cookbook = form.save(commit=False)
            cookbook.author = request.user
            cookbook.save()
            form.save_m2m()
            # message.success(request, 'Cookbook created!')
            return redirect(cookbook.get_absolute_url())
        else:
            return self.form_invalid(form)


class RecipeList(generic.ListView):
    """
    Renders the recipes page
    """
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'recipes.html'
    paginate_by = 6


@method_decorator(login_required, name='dispatch')
class AddRecipeView(generic.CreateView):
    model = Recipe
    # form_class = AddRecipeForm
    # fields = '__all__'
    template_name = 'add_recipe.html'
    fields = (
        'title',
        # 'author',
        'content',
        'featured_image',
        'categories',
        'time_to_cook')


@method_decorator(login_required, name='dispatch')
class EditRecipeView(LoginRequiredMixin, UpdateView):
    """
    Edit Recipe
    """
    model = Recipe
    template_name = 'edit_recipe.html'
    fields = ('title', 'content', 'categories', 'time_to_cook')


@method_decorator(login_required, name='dispatch')
class DeleteRecipeView(DeleteView):
    """
    Delete Recipe
    """
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('recipes')


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

    return HttpResponseRedirect(reverse(
        'recipe_detail', args=[comment.post.slug]
    ))


class EditComment(LoginRequiredMixin, UpdateView):
    """
    Edit Comment
    """
    model = Comment
    template_name = 'edit_comment.html'
    form_class = CommentForm


class RecipeLike(LoginRequiredMixin, View):
    """
    Like Recipe
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Recipe, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditProfilePageView(LoginRequiredMixin, UpdateView):
    """
    Edit User Profile
    """
    model = Profile
    template_name = 'edit_profile.html'
    fields = ('user', 'bio', 'image')
    success_url = reverse_lazy('home')


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
        return HttpResponseRedirect(reverse('home'))
