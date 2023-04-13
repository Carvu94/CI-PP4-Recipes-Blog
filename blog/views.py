from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from .models import Recipe, Category, Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView
from django.utils.decorators import method_decorator


def home(request):
    """
    Renders Home page
    """
    return render(request, "index.html")


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


class CategoriesList(generic.ListView):
    """
    Renders Categories page
    """
    model = Category
    template_name = 'categories.html'


class RecipeList(generic.ListView):
    """
    Renders the recipes page
    """
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'recipes.html'
    paginate_by = 6


class AddRecipeView(generic.CreateView):
    model = Recipe
    template_name = 'add_recipe.html'
    fields = (
        'title',
        'author',
        'content',
        'featured_image',
        'categories',
        'time_to_cook')


@method_decorator(login_required, name='dispatch')
class EditRecipeView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = 'edit_recipe.html'
    fields = ('title', 'content', 'categories', 'time_to_cook')


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
