from django.urls import path

from .views import Login, Reg, Logout


app_name='users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Reg.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
]