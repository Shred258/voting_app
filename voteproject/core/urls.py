from django.urls import path
from . import views

#app_name = 'polls'
urlpatterns = [
    path('', views.welcome, name='welcome'),  
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('poll/create/', views.create_poll_view, name='create_poll'),
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('poll/<int:poll_id>/results/', views.poll_result, name='poll_result'),
]
