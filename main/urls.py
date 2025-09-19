from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name='home') ,
    path('signup/' , views.signup_view , name="signup"),
    path('login/' ,views.Login_view, name='login'),
    path('profile/' , views.profile_view , name="profile"),
    path('logout/' , views.logout_view , name = "logout"),
    path('history/' , views.history_view , name='history'),
    path("withdraw/", views.withdraw_request_view, name="withdraw-request"),
    path('reset-password/', views.whatsapp_password_reset_request, name='password_reset'),
    path('withdraw-history' , views.withdraw_history_view , name='with-his'),
    path('profile/refer_history/' , views.refer_history , name='ref-his'),
    path('password-change' , views.Password_Change.as_view() , name='change_password')
]
