from django.urls import path

from . import views

# ADD NEW URLS WHEN NEW PAGES ARE CREATED, INCLUDING REDIRECTS
urlpatterns = [
    path("", views.index, name="index"),
    path("please_fucing_helpme", views.please_fucing_helpme, name="please_fucing_helpme"),
    path("create_acct", views.create_acct, name="create_acct"),
    path("create_new_account", views.create_new_account, name="create_new_account"),
    path("create_league", views.create_league, name="create_league"),
    path("create_team", views.create_team, name="create_team"),
    path("login", views.loginPage, name="login"),
    path("register", views.registerPage, name="register"),
]