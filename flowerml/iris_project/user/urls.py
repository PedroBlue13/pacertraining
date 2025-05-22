from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.logar, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.sair, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict_view, name='predict'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('history/', views.history_view, name='history'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy_view, name='privacy'),
]