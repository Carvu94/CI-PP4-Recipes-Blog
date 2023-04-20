from .models import Comment, Profile, Cookbook
from django import forms


class AddCookbookForm(forms.ModelForm):
    class Meta:
        model = Cookbook
        fields = (
            'title',
            'content',
            'recipes',
            # 'featured_image',
            )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            # 'featured_image': forms.ImageField(),
            'recipes': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


# class BookCommentForm(forms.ModelForm):
#     class Meta:
#         model = CookbookComment
#         fields = ('body',)


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }
