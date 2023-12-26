from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.add_post, name='add-post'),
    path('posts/', views.view_posts, name='view-posts'),
    path('posts/<slug:post_slug>/', views.view_post, name='view-post'),
    path('update-post/<slug:post_slug>/', views.update_post, name='update-post'),
]