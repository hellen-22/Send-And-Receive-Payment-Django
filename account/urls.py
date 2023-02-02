from django.urls import path 
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('home', views.home, name='home'),
    path('transaction', views.CreateTransactionView.as_view(), name='transaction')
]