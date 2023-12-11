from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('<int:pk>/report/', views.report, name='report'),
    path('playlist/', views.get_recommended_music_list, name='playlist'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_new/', views.PostCreate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]