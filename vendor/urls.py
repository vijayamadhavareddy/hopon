from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('check_username/', views.check_username, name="check_username"),
    path('send_email/', views.send_email, name="send_email"),
    path('verify_email/', views.verify_email, name="verify_email"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('forgot/', views.forgot, name="forgot"),
    path('chngpwd/', views.chngpwd, name="chngpwd"),
    path('logout/', views.logout, name="logout"),
    path('verifyaccount/', views.verifyaccount, name="verifyaccount"),
    path('verifysite/', views.verifysite, name="verifysite"),
]
