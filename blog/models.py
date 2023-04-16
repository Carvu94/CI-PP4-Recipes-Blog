from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify

STATUS = ((0, "Draft"), (1, "Published"))


class Category(models.Model):
    """
    Model for category

    """
    class Meta:
        verbose_name_plural = 'Categories'
    title = models.CharField(max_length=20)
    category_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """
    Model for recipe post
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    categories = models.ManyToManyField(Category)
    time_to_cook = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipes')

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    """
    Model for recipe comments
    """
    post = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[self.post.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')
