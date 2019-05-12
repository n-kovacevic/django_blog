from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/', views.PasswordChangeView.as_view(), name='password'),
    path('password_change_done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
