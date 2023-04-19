from .models import Comment, Profile, CookbookComment, Recipe
from django import forms


# class AddRecipeForm(forms.ModelForm):
#     class Meta:
#         model = Recipe
#         fields = (
#             'title',
#             'content',
#             'featured_image',
#             'categories',
#             'time_to_cook')

#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'content': forms.Textarea(attrs={'class': 'form-control'}),
#             'featured_image': forms.ImageField(),
#             'categories': forms.Select(attrs={'class': 'form-control'}),
#             'time_to_cook': forms.Textarea(attrs={'class': 'form-control'}),
#         }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class BookCommentForm(forms.ModelForm):
    class Meta:
        model = CookbookComment
        fields = ('body',)


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            # 'image': forms.ImageField
        }
