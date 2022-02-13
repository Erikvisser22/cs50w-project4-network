
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following/<int:user_id>", views.following, name="following"),
    
    # api routes
    path("new_post", views.new_post, name="new_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("save/<int:post_id>",views.save, name="save")
]
