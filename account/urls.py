from django.urls import path
from django.contrib.auth.decorators import login_required
from account import views, professor_views, teacher_view,student_view
from .views import update_profile_2

urlpatterns = [
    path('login', views.login_home, name='login'),  # Home page
    path('logout/', views.logout, name='logout'),  # Logout URL
    path('profile/', login_required(views.profile), name='profile'),  # Profile view with login required
    path('update/', login_required(views.update_profile), name='update-profile'),  # Update profile view with login required
    path('update-profile_2/', update_profile_2, name='update_profile_2'),  # Update profile 2 view
    # Professor views
    path('professor/home/', professor_views.professor_profile, name='professor_profiles'),
    
    # Teacher views
    path('teacher/home/', teacher_view.teacher_profile, name='teacher_profiles'),
    
     path('student/profiles/', student_view.student_profile, name='student_profiles'),
    # Uncomment these if needed
    # path('teacher/', views.teacher_profile, name='teacher_profiles'),
    # path('register/', views.register_profile, name='register_profiles'),
    # path('student/', views.student_profile, name='student_profiles'),
]
