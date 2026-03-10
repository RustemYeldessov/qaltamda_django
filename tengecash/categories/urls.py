from django.urls import path
from . import views

app_name = "categories"

urlpatterns = [
    path("create/", views.CategoryCreateView.as_view(), name="create"),
    path(
        "<int:pk>/update/",
        views.CategoryUpdateView.as_view(),
        name="update"
    ),
    path(
        "<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="delete"
    ),
    path(
        '<int:pk>/toggle-favorite/',
        views.category_toggle_favorite,
        name='toggle_favorite'
    ),
    path("", views.CategoryListView.as_view(), name="index"),
]