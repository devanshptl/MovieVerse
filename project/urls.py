
from django.contrib import admin
from django.urls import path,include
from app1.views import AdminStatsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/', AdminStatsView.as_view(), name='admin-stats'),
    path('watch/', include("app1.api.urls")),
    path('accounts/',include("accounts.urls")),
]
