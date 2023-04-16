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
     path('delete_recipe/<int:pk>', views.DeleteRecipeView.as_view(),
          name='delete_recipe'),
     path('add_recipe/', views.AddRecipeView.as_view(), name='add_recipe'),
     path('<slug:slug>/', views.RecipeDetail.as_view(), name="recipe_detail"),
     path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
     path('delete_comment/<int:comment_id>', views.delete_comment,
          name='delete_comment'),
     path('edit_comment/<int:pk>', views.EditComment.as_view(),
          name='edit_comment'),
     path('profile/<int:pk>', views.ProfilePageView.as_view(),
          name='profile_page'),
     path('edit_profile/<int:pk>/', views.EditProfilePageView.as_view(),
          name='edit_profile'),
     path('delete_profile/<int:pk>', views.DeleteUserProfile.as_view(),
          name='delete_profile'),
     path('create_profile', views.CreateProfileView.as_view(),
          name='create_profile'),


]
