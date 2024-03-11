from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

from core.customer import views as customer_views
from core.merchant import views as merchant_views

customer_urlpatterns = [
    path('', customer_views.home, name="home"),
    path('profile/', customer_views.profile_page, name="profile"),
]

merchant_urlpatterns = [
    path('', merchant_views.home, name="home"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),

    path('sign-in/', auth_views.LoginView.as_view(template_name="sign_in.html")),
    path('sign-out/', auth_views.LogoutView.as_view(next_page="/")),
    path('sign-up/', views.sign_up),

    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('merchant/', include((merchant_urlpatterns, 'merchant'))),
]
