from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import home, submit_request, track_request, account_info, register, user_login, manage_requests, update_request_status


urlpatterns = [
    path('', views.home, name='home'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('track-request/', views.track_request, name='track_request'),
    path('account-info/', views.account_info, name='account_info'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('manage_requests/', manage_requests, name='manage_requests'),
    path('update_request/<int:request_id>/', update_request_status, name='update_request'),
]


