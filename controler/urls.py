from django.urls import path
from .views import *
'''
urlpatterns = [
    path("withdraw-requests/", process_withdraw_requests, name="process-withdraw"),
    path("controller/", controller_page, name="balance-control"),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/approve/<int:user_id>/', approve_user, name='approve_user'),
    path('dashboard/decline/<int:user_id>/', decline_user, name='decline_user'),
    path('profile/' , admin_profile , name='admin-profile')

]
'''
urlpatterns = []
