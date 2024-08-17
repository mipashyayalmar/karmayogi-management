from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import UserProfile
from student.models import AcademicInfo
from teacher.models import PersonalInfo as TeacherPersonalInfo
from employee.models import PersonalInfo as EmployeePersonalInfo
from academic.models import ClassRegistration

@login_required(login_url='login')
def student_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['student']:
        # Display student's information
        try:
            student_info = AcademicInfo.objects.get(userprofile=user_profile)
        except AcademicInfo.DoesNotExist:
            student_info = None
        
        context = {
            'profile': user_profile,
            'student_info': student_info,
        }
        return render(request, 'student/home.html', context)
    
    elif user_profile.employee_type in ['teacher', 'professor']:
        # Handle teachers and professors the same as before
        return redirect('teacher_profiles')
    
    else:
        return HttpResponseForbidden("You do not have permission to view this page.")
