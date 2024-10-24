from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import UserProfile
from student.models import AcademicInfo
from teacher.models import PersonalInfo as TeacherPersonalInfo
from employee.models import PersonalInfo as EmployeePersonalInfo
from academic.models import ClassRegistration
from result.models import SubjectRegistration  # Import the SubjectRegistration model

@login_required(login_url='login')
def professor_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.employee_type != 'professor':
        return HttpResponseForbidden("You do not have permission to access this page.")

    # Fetch all subjects for the professor
    all_subjects = SubjectRegistration.objects.all()  # Get all subjects

    total_student = AcademicInfo.objects.count()
    total_teacher = TeacherPersonalInfo.objects.count()
    total_employee = EmployeePersonalInfo.objects.count()
    total_class = ClassRegistration.objects.count()

    context = {
        'student': total_student,
        'teacher': total_teacher,
        'employee': total_employee,
        'total_class': total_class,
        'profile': user_profile,
        'all_subjects': all_subjects,  # Pass subjects to the template
    }

    return render(request, 'professor/home.html', context)
