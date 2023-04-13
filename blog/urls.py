from . import views
from django.urls import path


urlpatterns = [

     path('', views.home, name="home"),
     path('about', views.about, name="about"),
     path('recipes/', views.RecipeList.as_view(), name="recipes"),
     path('categories/', views.CategoriesList.as_view(), name="categories"),
     path('contact', views.contact_us, name="contact"),
     path('edit_recipe/<int:pk>', views.EditRecipeView.as_view(),
          name='edit_recipe'),
     path('add_recipe/', views.AddRecipeView.as_view(), name='add_recipe'),
     path('<slug:slug>/', views.RecipeDetail.as_view(), name="recipe_detail"),
     path('delete_comment/<int:comment_id>', views.delete_comment,
          name='delete_comment'),
     path('edit_comment/<int:pk>', views.EditComment.as_view(),
          name='edit_comment'),
 ]
