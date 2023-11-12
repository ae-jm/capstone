from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path("mypage/", views.mypage, name='mypage'),
    path("delete/", views.delete, name='delete'),
    path("update/", views.update, name='update'),
    path("update/password/", views.change_password, name='change_password'),
]