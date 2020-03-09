from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('user_login/',views.user_login,name='user_login'),
    # path('login/',views.login,name = 'login'),
]
