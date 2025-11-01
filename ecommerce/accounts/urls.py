from django.urls import path
from .views import register, login_view, logout
from .views.preview import preview_welcome_email
from .views.profile import profile

app_name = 'accounts'  # Add namespace

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('preview/welcome-email/', preview_welcome_email, name='preview_welcome_email'),
]