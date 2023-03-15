from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index, name = "Base"),
    path('home',views.Login, name = "Home"),
    path('signup', views.SignUp, name = "SignUp"),
    path('Home', views.Transfer, name = 'Home'),
    path('update', views.Update, name='Update'),
    path('logout', views.Logout, name='Logout'),
    path('return', views.Return, name='Return'),
    path('dashboard', views.Dash, name='Dashboard'),
    path('prediction', views.Prediction, name="Prediction")
]