from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("create/", views.UserCreateView.as_view(), name="create"),
    path(
        "<int:pk>/update/",
        views.UserUpdateView.as_view(),
        name="update"
    ),
    path(
        "<int:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="delete"
    ),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),

    path("", views.UserListView.as_view(), name="index"),
]