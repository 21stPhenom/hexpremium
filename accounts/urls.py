from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login-only/', views.login_only, name='login_only'),
    path('upgrade-plan/', views.upgrade_plan, name='upgrade_plan')
]