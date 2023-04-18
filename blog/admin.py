from django.contrib import admin
from .models import Recipe, Category, Comment, Profile, Cookbook
from django_summernote.admin import SummernoteModelAdmin


admin.site.register(Profile)


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    """
    Add fields in admin panel using summernote editor
    """
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Add fields for Category in admin panel
    """
    list_display = ['title']
    search_fields = ['title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Add fields for Category in admin panel
    """
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Cookbook)
class CookbookAdmin(admin.ModelAdmin):
    """
    Add fields for Cookbook in admin panel
    """
    list_display = ('author', 'created_on', 'title', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['author', 'title']
