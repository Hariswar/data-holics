from django.urls import path

from . import views

# ADD NEW URLS WHEN NEW PAGES ARE CREATED, INCLUDING REDIRECTS
urlpatterns = [
    path("", views.index, name="home"),
    path("please_fucing_helpme", views.please_fucing_helpme, name="please_fucing_helpme"),
    path("create_acct", views.create_acct, name="create_acct"),
    path("create_new_account", views.create_new_account, name="create_new_account"),
    path("create_league", views.create_league, name="create_league"),
    path("create_new_league", views.create_new_league, name="create_new_league"),
    path("create_new_league", views.create_new_league, name="create_new_league"),
    path("create_team", views.create_team, name="create_team"),
    path("login", views.loginPage, name="login"),
    path("log_out", views.logoutUser, name="log_out"),
    path("register", views.registerPage, name="register"),
    path("create_new_team", views.create_new_team, name="create_new_team"),
    path("user_home", views.user_home, name="user_home"),
    path("create_sport", views.create_new_sport, name="create_sport"),
    path("create_game", views.create_game, name="create_game"),
    path("display_stats", views.display_stats, name="display_stats"),
]