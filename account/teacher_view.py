from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import UserProfile
from student.models import AcademicInfo
from teacher.models import PersonalInfo as TeacherPersonalInfo
from employee.models import PersonalInfo as EmployeePersonalInfo
from academic.models import ClassRegistration
from result.models import SubjectRegistration
 
@login_required(login_url='login')
def teacher_profile(request, teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.employee_type in ['teacher', 'professor']:
        # Fetch teacher profile based on ID or current user
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)

        # Check if the teacher can view the profile
        if teacher.address.userprofile == user_profile or user_profile.employee_type in ['teacher', 'professor']:
            # Fetch all necessary counts and data
            all_teachers = TeacherPersonalInfo.objects.all()
            total_student = AcademicInfo.objects.count()
            total_teacher = TeacherPersonalInfo.objects.count()
            total_employee = EmployeePersonalInfo.objects.count()
            total_class = ClassRegistration.objects.count()
            total_subjects = SubjectRegistration.objects.filter(userprofile=user_profile)

            context = {
                'teacher': teacher,
                'profile': user_profile,
                'all_teachers': all_teachers,
                'student': total_student,
                'teacher_count': total_teacher,
                'employee': total_employee,
                'total_class': total_class,
                'total_subjects': total_subjects,  # Now this is a queryset, not just a count
                'subject_count': total_subjects.count(),  # To display the total number of subjects
            }
            return render(request, 'teacher/home.html', context)
        else:
            return HttpResponseForbidden("You do not have permission to view this profile.")
    else:
        return HttpResponseForbidden("You do not have permission to view this page.")
