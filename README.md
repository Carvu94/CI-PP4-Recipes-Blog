# Hungry Chef

(Developer: Matej Car)


![PP4](/)


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
- As a registered user I can create a cookbook so that I can add recipes that I like!!!!!
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
- As a site admin I can delete or update user's comments so that I manage my content!!!!!
- As a site admin I can delete or update user's cookbooks so that I can manage my content!!!!
- As a site admin I can create draft recipes so that I can finish writing the content later
- As a site admin I can create, update and delete categories so that I can manage my blog content

### Agile Methodology




[Back to Table Of Contents](#table-of-contents)


# Features


## Existing Features






[Back to Table Of Contents](#table-of-contents)


## Future Features




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


- Libraries:


- Other:


### Frameworks & Tools


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

