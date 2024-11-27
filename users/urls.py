from django.urls import path
from .views import register, user_login, user_logout

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('dashboard/', user_dashboard, name='user_dashboard'),  # Dashboard for regular users
    # path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]
