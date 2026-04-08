from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import IndexView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("users/", include(("qaltamda.users.urls", "users"), namespace="users")),
    path("categories/", include(("qaltamda.categories.urls", "categories"), namespace="categories")),
    path("sections/", include(("qaltamda.sections.urls", "sections"), namespace="sections")),
    path("expenses/", include(("qaltamda.expenses.urls", "expenses"), namespace="expenses")),
    path("analytics/", include(("qaltamda.analytics.urls", "analytics"), namespace="analytics")),

    path("", IndexView.as_view(), name='index'),

    path('api-auth/', include('rest_framework.urls'))
]
