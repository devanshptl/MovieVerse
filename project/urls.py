
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include("app1.api.urls")),
    path('accounts/',include("accounts.urls")),
]
