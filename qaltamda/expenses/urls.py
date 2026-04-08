from django.urls import path
from . import views
from .api_views import ExpenseAPIView


app_name = "expenses"

urlpatterns = [
    path("<int:pk>/detail/", views.ExpenseDetailView.as_view(), name="show"),
    path("create/", views.ExpenseCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.ExpenseUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.ExpenseDeleteView.as_view(), name="delete"),
    path("api/", ExpenseAPIView.as_view(), name="expense-api"),
    path("", views.ExpenseListView.as_view(), name="index")
]