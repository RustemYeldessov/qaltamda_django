from django.urls import path
from . import views

app_name = "sections"

urlpatterns = [
    path("create/", views.SectionCreateView.as_view(), name="create"),
    path(
        "<int:pk>/update/",
        views.SectionUpdateView.as_view(),
        name="update"
    ),
    path(
        "<int:pk>/delete/",
        views.SectionDeleteView.as_view(),
        name="delete"
    ),
    path("", views.SectionListView.as_view(), name="index")
]