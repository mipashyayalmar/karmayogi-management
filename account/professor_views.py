from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import UserProfile
from student.models import AcademicInfo
from teacher.models import PersonalInfo as TeacherPersonalInfo
from employee.models import PersonalInfo as EmployeePersonalInfo
from academic.models import ClassRegistration
<<<<<<< HEAD
from result.models import SubjectRegistration  # Import the SubjectRegistration model
=======
from result.models import SubjectRegistration  # Import your Subject model

@login_required(login_url='login')
def teacher_profile(request, teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['teacher', 'professor']:
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)

        if teacher.address.userprofile == user_profile or user_profile.employee_type == 'professor':
            all_teachers = TeacherPersonalInfo.objects.all()
            total_student = AcademicInfo.objects.count()
            total_teacher = TeacherPersonalInfo.objects.count()
            total_employee = EmployeePersonalInfo.objects.count()
            total_class = ClassRegistration.objects.count()
            total_subjects = SubjectRegistration.objects.all()  # Get all subjects

            context = {
                'teacher': teacher,
                'profile': user_profile,
                'all_teachers': all_teachers,
                'student': total_student,
                'teacher_count': total_teacher,
                'employee': total_employee,
                'total_class': total_class,
                'total_subjects': total_subjects,  # Add total subjects to context
            }
            return render(request, 'teacher/home.html', context)
        else:
            return HttpResponseForbidden("You do not have permission to view this profile.")
    else:
        return HttpResponseForbidden("You do not have permission to view this page.")
>>>>>>> 29f2085b916bc7ee9553cfc80f3870a0d2da48b6

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
    total_subjects = SubjectRegistration.objects.all()  # Get all subjects

    context = {
        'student': total_student,
        'teacher': total_teacher,
        'employee': total_employee,
        'total_class': total_class,
        'profile': user_profile,
<<<<<<< HEAD
        'all_subjects': all_subjects,  # Pass subjects to the template
=======
        'profiles': professor_profiles,
        'total_subjects': total_subjects,  # Add total subjects to context
>>>>>>> 29f2085b916bc7ee9553cfc80f3870a0d2da48b6
    }

    return render(request, 'professor/home.html', context)
