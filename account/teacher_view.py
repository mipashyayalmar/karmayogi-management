from django.shortcuts import render, get_object_or_404
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
    """Allows principals, professors, or individual teachers to view teacher profiles."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the user is a principal, professor, or the teacher themselves
    if user_profile.employee_type not in ['teacher', 'professor', 'principal']:
        return HttpResponseForbidden("You do not have permission to view this page.")

    if teacher_id:
        teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)
    else:
        teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)

    # Restrict teachers from viewing other teachers' profiles unless they are professors/principals
    if teacher.address.userprofile != user_profile and user_profile.employee_type not in ['professor', 'principal']:
        return HttpResponseForbidden("You do not have permission to view this profile.")

    # Fetch necessary data for the dashboard
    all_teachers = TeacherPersonalInfo.objects.all()
    total_student = AcademicInfo.objects.count()
    total_teacher = TeacherPersonalInfo.objects.count()
    total_employee = EmployeePersonalInfo.objects.count()
    total_class = ClassRegistration.objects.count()

    # Subjects assigned to the teacher
    assigned_subjects = SubjectRegistration.objects.filter(userprofile=teacher.address.userprofile)
    subject_count = assigned_subjects.count()

    context = {
        'teacher': teacher,
        'profile': user_profile,
        'all_teachers': all_teachers,
        'student': total_student,
        'teacher_count': total_teacher,
        'employee': total_employee,
        'total_class': total_class,
        'total_subjects': assigned_subjects,
        'subject_count': subject_count,
    }

    return render(request, 'teacher/home.html', context)
