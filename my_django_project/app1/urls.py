from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL (homepage)
    path('register/', views.registration_view, name='user_registration'),  # User Registration
    path('ngo-register/', views.ngo_registration, name='ngo_registration'),  # NGO Registration
    path('event-register/', views.event_register, name='event_register'),  # Event Registration Route
    path('volunteer/', views.volunteer_form_view, name='volunteer_form'),  # Volunteer Form Route
    path('volunteers-list/', views.volunteers_list_view, name='volunteers_list'),  # Volunteers List Route
    path('contact_form/', views.contact_form_view, name='contact_form'),
    path('login/', views.user_login, name='user_login'),
    path('ngo-login/', views.ngo_login, name='ngo_login'),
    path('health_tracker/', views.health_tracker, name='health_tracker'),  # Health Tracker Route
    path('profile/', views.profile, name='profile'),  # User Profile
    path('logout/', views.logout, name='logout'),
    path('help-request/', views.help_request_form, name='help_request_form'),
    path('submit-help-request/', views.submit_help_request, name='submit_help_request'),
    path('view-help-requests/', views.view_help_requests, name='view_help_requests'),
]
