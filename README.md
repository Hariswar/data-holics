# Leaguify

## Setting Up the Database

### Initial Setup 

- The current database is set up at *main.db* and ready to be used. 
- Simply use *./setup_db.sh* to set up the initial database if a reset is necessary.
- ***WARNING:** DOING THIS DELETES ALL DATA IN THE CURRENT DATABASE!*

### Database Migration

- Full database migration should not be necessary because all changes made to our database setup will be done in SQL.

### Steps To Install The System On Another Computer

- First, we must clone the git repository.
- Next, we have to setup the virtual environment.
    - python3 -m venv venv.
    - source venv/bin/active.
- Then, we must install Django.
    - pip install Django
- Then we need to run the migrations.
    - python manage.py migrate
- Finally, we can run the server.
    - python manage.py runserver
- If you follow these steps, you should be able to run our website with no issues. 

## Creating Models, Pages, and Database Functions

### Creating A Model

- Creating a model is done in *leaguify/models.py*
- Setup the model class to have the same name as the database entity.
    - All attributes must also share the same name.
    - Make sure to define attribute constraints in the model as well.
- Once the model is set up, you can now use it in *leaguify/views.py* to include the entity data in your views.

### Creating Database Functions

- All database functions will be defined in *leaguify/views.py*
- When creating a page that will be visible to the user via HTML, copy any example used in the HTML PAGE VIEWS section. 
    - Make sure this returns a render (or redirect).
    - If render includes database data, include it in **context** as shown in *league.html*
- When creating a function that updates the database and is hidden from the user, copy any example in the DATABASE FUNCTIONS + REDIRECTS section.
    - Make sure this returns a redirect.
- When creating either, add the page name to *leaguify/urls.py* similarly to other URLs.

### Creating New HTML Pages

- In the *leaguify/templates* folder, create a new HTML page or make a copy of an old one. 
- Reference other pages for help in defining database use functions.

## Other Tips

- There are helpful django links in many of the python files throughout the project. 
- If using Visual Studio Code, there are several extensions available to view the SQLite database as a table.
- Google is epic.
- w3schools/GeeksForGeeks may also be helpful .
