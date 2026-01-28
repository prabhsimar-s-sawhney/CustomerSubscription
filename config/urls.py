from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # API routes
    # path("api/users/", include("apps.users.urls")),

    # later:
    # path("api/orders/", include("apps.orders.urls")),
]
