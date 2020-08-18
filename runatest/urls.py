from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="api-auth/", view=include("rest_framework.urls")),
    path(route="api/", view=include("categories.urls")),
]
