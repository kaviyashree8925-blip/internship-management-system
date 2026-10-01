from django.urls import path
from . import views
urlpatterns = [path('', views.dashboard, name='dashboard'),path('register/', views.register, name='register'),path('login/', views.login_view, name='login'),path('logout/', views.logout_view, name='logout'),path('internships/', views.internships, name='internships'),path('internships/<int:pk>/apply/', views.apply, name='apply'),path('profile/', views.profile, name='profile')]
