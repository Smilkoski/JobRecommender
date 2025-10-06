from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile/', views.profile_update, name='profile_update'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    # DRF API paths
    path('api/jobs/', views.JobAPIView.as_view(), name='api_jobs_list_create'),
    path('api/profiles/', views.ProfileAPIView.as_view(), name='api_profiles_list_create'),
]