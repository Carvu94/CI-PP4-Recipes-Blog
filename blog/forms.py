from .models import Comment, Profile
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            # 'image': forms.ImageField
        }
