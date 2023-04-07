from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('categories/', views.CategoriesList.as_view(), name="categories"),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
 ]
