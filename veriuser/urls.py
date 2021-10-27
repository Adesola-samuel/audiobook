from django.urls import path
from . import views

app_name = 'veriuser'
urlpatterns = [
    path('Login/', views.login_page, name='login'),
    path('Sign-up/', views.create_user, name='create_user'),
    path('Logout/', views.logout_user, name='logout'),

]