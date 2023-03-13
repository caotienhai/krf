from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'userprofile'

urlpatterns = [
    path('myaccount/', views.myaccount, name='myaccount'),
    path('sign-up/', views.signup, name='signup'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('profile-update/', views.profile_update, name='profile_update'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='userprofile/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='userprofile/password_reset_complete.html'), name='password_reset_complete'),
]
