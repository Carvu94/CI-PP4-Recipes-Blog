# Hungry Chef

Hungry Chef is a blog web site.
(Developer: Matej Car)


![PP4](/docs/images/am-i-responsive.png)


[ >>> Live live website ]()


## Table of Contents
- [**User Experience**](#user-experience)
- [**Features**](#features)
   - [Existing Features](#existing-features)
   - [Future Features](#future-features)
- [**Technical Design**](#technical-design)
   - [Agile Design](#agile-design)
   - [Data Model](#data-model)
   - [Wireframes](#wireframes)
- [**Technologies Used**](#technologies-used)
   - [Frameworks & Tools](#frameworks--tools)
- [**Validation**](#validation)
   - [Testing](#testing)
- [**Bugs**](#bugs)
   - [Solved Bugs](#solved-bugs)
   - [Remaining Bugs](#remaining-bugs)
- [**Deployment**](#deployment)
- [**Credits**](#credits)




# User Experience

### **User Stories**

#### **Site User**
- As a user I can view a paginated list of recipes so that I can pick one to read
- As a user I can view a selection of random recipes so that I can pick and read the one I like
- As a user I can click on a recipe so that I can read the whole recipe
- As a user I can view the comments on individual recipes so that I can read other user's opinions on recipes
- As a user I can register for an account so that I can interact with content and post recipes
- As a user I can view and select a category of recipes so that I can view recipes in category
- As a user I can search the recipes by keyword so that find relative recipes
- As a user I can view the number of likes so that I can see which recipe is most popular
- As a user I can view other people cookbooks so that I can get ideas

#### **Registered User**
- As a registered user I can post a comment on a recipe so that I can be involved in the conversation
- As a registered user I can like/unlike the recipes so that I can interact with the content
- As a registered user I can login so that I can access my content
- As a registered user I can logout so that other users cannot access my account
- As a registered user I can access my profile so that I can edit my details and upload a profile image
- As a registered user I can delete my comments so that the comments are no longer visible
- As a registered user I can edit my comments so that I can update my comments
- As a registered user I can create a cookbook so that I can add recipes that I like
- As a registered user I can add a recipe to my cookbook so that I can easily find the recipes
- As a registered user I can edit my cookbook so that I can change the list of recipes
- As a registered user I can delete my cookbook so that my cookbook is no longer visible
- As a registered user I can like/unlike the books so that express my opinion
- As a registered user I can post a comment on a recipe so that interact with a user that posted
- As a registered user I can add the recipe on the blog so that other people can see and share their opinion
- As a registered user I can edit my recipe so that update my recipe
- As a registered user I can delete my recipe so that it is not visible to other users

#### **Site Admin**
- As a site admin I can approve/disapprove the comments so that I can decide if the content is relevant
- As a site admin I can create, read, update, and delete recipes so that I can manage my content
- As a site admin I can delete or update user's comments so that I can manage my content
- As a site admin I can delete or update user's cookbooks so that I can manage my content
- As a site admin I can create draft recipes so that I can finish writing the content later
- As a site admin I can create, update and delete categories so that I can manage my blog content

### Agile Methodology




[Back to Table Of Contents](#table-of-contents)


# Features

## Existing Features


### Nav-bar and Logo

- this feature is present throughout entire project except on a page where user is prompt to define his profile role for using the app, and since the incentive is to pick the role as its vital part of a user functionality of the web app I decided to not incude this feature in this part of the project.

- page logo is also a link to home page. Other than that, navbar consists of links to: Home page, About Us, Recipes, Cookbooks, Categories, and Contact Us pages.

- authenticated user has his username visible on the navbar which is a link to profile page.

- unauthenticated user can see links to Register/Login instead of username.

- this feature also contains search bar to quickly search recipes by keyword.


![Nav-bar](/docs/features/nav_bar.png)

### Home Page

- this feature contains the carousel for aesthetis, and top recipes. The Carousel is present throughout the whole project.

- Top recipes are listed based on number of likes. This way users are able to see few best recipes straight away. 

- Users are also able to see recipe card that contains number of likes and comments. 

![Carousel](/docs/features/carousel.png)

![Home Page](/docs/features/top_recipes.png)

### Footer 

- This feature contains a quote from Hungry Chef, Contact information and copyright.

- This feature si present throughout the whole project

![Footer](/docs/features/footer.png)

### About us

- This feature gives more information to users regarding the blog.

- This feature also contains fun facts regarding food. 

![About us](/docs/features/about_us_page.png)

### Recipes

- This feature lists all recipes on blog.

- This feature allows authenticated users to create recipe. unverified users will not be able to see this option. 

- This feature also contains recipe cards with picutres, author name, recipe title, date posted, number of likes and comments. 

- This feature allows users to access the recipe details. 

![Recipes](/docs/features/recipes_page.png)

### Recipe detail

- This feature allows user to see all recipe details and comments section.

- authenticated users will be able to like and comment posts.

- if authenticated user is owner of recipe, he will be able to see Edit/Delete buttons

![Recipe Detail](/docs/features/recipe_detail.png)

### Add recipe

- This feature allows authenticated users to create their own recipe. 

- unverified users are not able to access this page. 

- Before recipes are posted, they must be approved by admin. 

![Recipe Add](/docs/features/add_recipe.png)

### Edit recipe

- This feature allows authenticated users to edit their own recipe. Users are not able to edit other users recipes.

- unverified users are not able to access this page. 

![Recipe Edit](/docs/features/edit_recipe.png)

### Delete recipe

- This feature allows authenticated users to delete their own recipe. Users are not able to delete other users recipes.

- unverified users are not able to access this page. 

![Recipe Delete](/docs/features/dlt-confirm.png)

### Comments

- This feature allows authenticated users to interact with recipes and leave their comments. 

- Before comments are posted, they must be approved by admin. 

- Users are able to edit and delete their own comments. 

![Comments](/docs/features/comments_section.png)

### Edit comments

- This feature allows authenticated users that are owner of comments to edit them. 

![Comment Edit](/docs/features/comment_edit_msg.png)

### Delete comments

- This feature allows authenticated users that are owner of comments to delete them. 

![Delete Comment](/docs/features/dlt-comment-modal.png)

### Prev & Next buttons

- This feature allows users to change pages on recipes and cookbooks pages. 

![Prev & Next Button](/docs/features/prev_next_btn.png)

### Cookbooks

- This feature allows users too see cookbooks that other users created.

- Users are able to see cookbook picture, author, title, description, date created and number of likes. 

- Authenticated users will see a button to create their own cookbook. 

- unverified users will not be able to see the button to create cookbook.

![Cookbooks](/docs/features/cookbooks_page.png)

### Add Cookbook

- This feature allows authenticated users to create cookbook. 

- Before cookbook is posted, it must be approved by admin.

![Cookbook Add](/docs/features/create_cookbook.png)

### Edit Cookbook

- This feature allows authenticated users to edit their own cookbook.  

![Cookbook Edit](/docs/features/edit_book.png)

### Categories

- This feature allows users to see categories that admin set.

- Admin is able to create, edit and delete categories through admin panel.

- This feature allows users to pick a category of food that they desire and see all recipes in that category. 

![Categories](/docs/features/categories_list.png)

### Category results

- This feature lists all recipes in chosen category. 

![Category Results](/docs/features/category_result.png)

### Contact Us

- This feature is a form that allows users to contact owner of the Hungry Chef and give feedback or query. 

![Contact us](/docs/features/contact_us.png)

### Register

- This feature allows users to register for a profile to be able to post recipes, create cookbooks and comment. 

![Register](/docs/features/sign-up.png)

### Login

- This feature allows existing users to login to be able to interact with content.

![Login](/docs/features/sign-in.png)

### Profile

- This feature allows registered users to update their profile bio or image. 

- unverified users are able to see profile pages of other users. 

![Profile](/docs/features/profile.png)

### Edit profile

- This feature allows authenticated users to edit or delete their profile.

![Edit Profile](/docs/features/edit_profile.png)

### Search

- This feature allows all users to search for recipes by keywords. 

![Search](/docs//features/search_results.png)

### Messages

- Messages are available for all user actions to inform users on success of their actions. 

![Message1](/docs/features/add_recipe_msg.png)
![Message2](/docs/features/comment_msg.png)
![Message3](/docs/features/edit_recipe_msg.png)
![Message4](/docs/features/sign_in_msg.png)
![Message5](/docs/features/recipe-edit-msg.png)
![Message6](/docs/features/comment_edit_msg.png)
![Message7](/docs/features/create_cookbook_msg.png)
![Message8](/docs/features/delete_profile_msg.png)
![Message9](/docs/features/dlt-comment-msg.png)
![Message10](/docs/features/recipe-del-msg.png)


[Back to Table Of Contents](#table-of-contents)


## Future Features

 - Categories drop-down list in Nav-Bar
   - This feature would give users faster access to wanted categories.

- Comments on Cookbooks
   - This feature would give authenticated users option to express their opinion on other users cookbooks.

- Add to Cookbook button
   - This feature would be possible for authenticated users that have cookbooks. 
   - This feature would allow users to add recipes to their cookbook without having to go to edit cookbook. 

- Text formatting for recipes and cookbooks
   - This feature would create a much better look for blog


## Technical Design


### Agile Design


### Data Model

For creating data diagram I was using Lucidchart

![Data Model](/docs/images/ER%20Diagram%20Hungry%20Chef.png)

### Wireframes

For creating wireframes I was using Balsamiq.

#### **Home Page**
![Home Page](/docs/images/Home%20page.png)

#### **About Page**
![About Page](/docs/images/About%20Page.png)

#### **Recipes Page**
![Recipes Page](/docs/images/Recipes%20page.png)

#### **Cookbooks Page**
![Cookbooks Page](/docs/images/Cookbook%20page.png)

#### **Contact Us Page**
![Contact Page](/docs/images/Contact%20page.png)

#### **Categories Page**
![Categories Page](/docs/images/Categories.png)

#### **Recipe Detail Page**
![Recipe Detail](/docs/images/Recipe%20details%20page.png)

#### **Cookbook Detail Page**
![Cookbook Detail](/docs/images/cookbook%20details%20page.png)

#### **Register Page**
![Register Page](/docs/images/Register%20page.png)

#### **Sign In Page**
![Sing In](/docs/images/Sign%20In%20page.png)

#### **Profile Page**
![Profile Page](/docs/images/Profile%20page.png)

#### **Search Results Page**
![Search Results](/docs/images/Search%20result%20page%20(cookbook%20and%20recipes).png)

## Technologies Used


- Languages:
   - HTML
   - CSS
   - Javascript
   - Boostrap
   - Python
   - Django 

- Libraries & Technologies:

   - [Am I Responsive](http://ami.responsivedesign.is/) 
   - [Balsamiq](https://balsamiq.com/) 
   - [Bootstrap 4.2](https://getbootstrap.com/). 
   - [Cloudinary](https://cloudinary.com/) 
   - [Lucidcharts](https://lucid.app/) 
   - [Favicon.io](https://favicon.io)
   - [Chrome dev tools](https://developers.google.com/web/tools/chrome-devtools/)
   - [Boostrap icons](https://fontawesome.com/) 
   - [Git](https://git-scm.com/) 
   - [GitHub](https://github.com/)
   - [Google Fonts](https://fonts.google.com/)   

- Other:


[Back to Table Of Contents](#table-of-contents)


## Validation


## Testing


[Back to Table Of Contents](#table-of-contents)


# Bugs


## Solved Bugs

**Integrity Bug**

When submitting new post, the following error was returned: 

*duplicate key value violates unique constraint "blog_recipe_slug_key"
DETAIL: Key (slug)=() already exists.*

After some research, I added 'slugify' method to the recipe model and redirected the user to the recipes page.


## Remaining Bugs

**Admin Post Deletion**

When the admin is deleting comments from the page view, the wrong comment is deleted.


## Deployment


[Back to Table Of Contents](#table-of-contents)


## Credits


### Code


## Acknowledgements




[Back to Table Of Contents](#table-of-contents)

