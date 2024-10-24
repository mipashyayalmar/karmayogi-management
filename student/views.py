from academic.models import ClassRegistration
from account.models import UserProfile
from .forms import *
from .models import *
from django.db.models import Q
from .forms import StudentSearchForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AcademicInfo
import logging
from teacher.models import PersonalInfo as TeacherPersonalInfo

def load_upazilla(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor','teacher'])

    # if user_profile.employee_type != 'professor':
    #     return redirect('login')
    district_id = request.GET.get('district')
    upazilla = Upazilla.objects.filter(district_id=district_id).order_by('name')

    upazilla_id = request.GET.get('upazilla')
    union = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
    context = {
        'profile' : user_profile,
        'upazilla': upazilla,
        'union': union
    }
    return render(request, 'others/upazilla_dropdown_list_options.html', context)


def class_wise_student_registration(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor','teacher'])

    # if user_profile.employee_type != 'professor':
    #     return redirect('login')
    register_class = ClassRegistration.objects.all()
    context = {
        'register_class': register_class,
        'profile' : user_profile,
        }
    return render(request, 'student/class-wise-student-registration.html', context)

def student_registration(request,teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['teacher', 'professor']:
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)

    # if user_profile.employee_type != 'professor':
    #     return redirect('login')
        
    academic_info_form = AcademicInfoForm(request.POST or None)
    personal_info_form = PersonalInfoForm(request.POST or None, request.FILES or None)
    student_address_info_form = StudentAddressInfoForm(request.POST or None)
    guardian_info_form = GuardianInfoForm(request.POST or None)
    emergency_contact_details_form = EmergencyContactDetailsForm(request.POST or None)
    previous_academic_info_form = PreviousAcademicInfoForm(request.POST or None)
    previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST or None, request.FILES)

    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor','teacher'])

        # if user_profile.employee_type != 'professor':
        #     return redirect('login')
        if academic_info_form.is_valid() and personal_info_form.is_valid() and student_address_info_form.is_valid() and guardian_info_form.is_valid() and emergency_contact_details_form.is_valid() and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
            s1 = personal_info_form.save()
            s2 = student_address_info_form.save()
            s3 = guardian_info_form.save()
            s4 = emergency_contact_details_form.save()
            s5 = previous_academic_info_form.save()
            s6 = previous_academic_certificate_form.save()
            academic_info = academic_info_form.save(commit=False)
            academic_info.personal_info = s1
            academic_info.address_info = s2
            academic_info.guardian_info = s3
            academic_info.emergency_contact_info = s4
            academic_info.previous_academic_info = s5
            academic_info.previous_academic_certificate = s6
            academic_info.save()
            return redirect('student-list')

    context = {
        'teacher': teacher,
        'profile' : user_profile,
        'academic_info_form': academic_info_form,
        'personal_info_form': personal_info_form,
        'student_address_info_form': student_address_info_form,
        'guardian_info_form': guardian_info_form,
        'emergency_contact_details_form': emergency_contact_details_form,
        'previous_academic_info_form': previous_academic_info_form,
        'previous_academic_certificate_form': previous_academic_certificate_form
    }
    return render(request, 'student/student-registration.html', context)

def student_list(request,teacher_id=None):
    # teacher img start here with id none add in it teacher = teacher in context
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['teacher', 'professor']:
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)

    # if user_profile.employee_type != 'professor':
    #     return redirect('login')

    form = StudentSearchForm(request.GET or None)
    student_name = request.GET.get('name', None)
    queries = Q(is_delete=False)

    if student_name:
        queries &= Q(personal_info__name__icontains=student_name)

    student = AcademicInfo.objects.filter(queries).order_by('-id')

    context = {
        'teacher': teacher,
        'form': form,
        'student': student,
        'profile': user_profile,
    }
    return render(request, 'student/student-list.html', context)

def student_profile(request, reg_no ,teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['teacher', 'professor']:
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)

    # if user_profile.employee_type != 'professor':
    #     return redirect('login')

    student = AcademicInfo.objects.get(registration_no=reg_no)
    context = {
        'teacher': teacher,
        'profile' : user_profile,
        'student': student
    }
    return render(request, 'student/student-profile.html', context)

def student_edit(request, reg_no ,teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['teacher', 'professor']:
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)
    # if user_profile.employee_type != 'professor':
    #     return redirect('login')
    
    student = AcademicInfo.objects.get(registration_no=reg_no)
    academic_info_form = AcademicInfoForm(instance=student)
    personal_info_form = PersonalInfoForm(instance=student.personal_info)
    student_address_info_form = StudentAddressInfoForm(instance=student.address_info)
    guardian_info_form = GuardianInfoForm(instance=student.guardian_info)
    emergency_contact_details_form = EmergencyContactDetailsForm(instance=student.emergency_contact_info)
    previous_academic_info_form = PreviousAcademicInfoForm(instance=student.previous_academic_info)
    previous_academic_certificate_form = PreviousAcademicCertificateForm(instance=student.previous_academic_certificate)

    if request.method == 'POST':
        academic_info_form = AcademicInfoForm(request.POST, instance=student)
        personal_info_form = PersonalInfoForm(request.POST, request.FILES, instance=student.personal_info)
        student_address_info_form = StudentAddressInfoForm(request.POST, instance=student.address_info)
        guardian_info_form = GuardianInfoForm(request.POST, instance=student.guardian_info)
        emergency_contact_details_form = EmergencyContactDetailsForm(request.POST, instance=student.emergency_contact_info)
        previous_academic_info_form = PreviousAcademicInfoForm(request.POST, instance=student.previous_academic_info)
        previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST, request.FILES, instance=student.previous_academic_certificate)
        if academic_info_form.is_valid() and personal_info_form.is_valid() and student_address_info_form.is_valid() and guardian_info_form.is_valid() and emergency_contact_details_form.is_valid() and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
            s1 = personal_info_form.save()
            s2 = student_address_info_form.save()
            s3 = guardian_info_form.save()
            s4 = emergency_contact_details_form.save()
            s5 = previous_academic_info_form.save()
            s6 = previous_academic_certificate_form.save()
            academic_info = academic_info_form.save(commit=False)
            academic_info.personal_info = s1
            academic_info.address_info = s2
            academic_info.guardian_info = s3
            academic_info.emergency_contact_info = s4
            academic_info.previous_academic_info = s5
            academic_info.previous_academic_certificate = s6
            academic_info.save()
            return redirect('student-list')

    context = {
        'teacher': teacher,
        'profile' : user_profile,
        'academic_info_form': academic_info_form,
        'personal_info_form': personal_info_form,
        'student_address_info_form': student_address_info_form,
        'guardian_info_form': guardian_info_form,
        'emergency_contact_details_form': emergency_contact_details_form,
        'previous_academic_info_form': previous_academic_info_form,
        'previous_academic_certificate_form': previous_academic_certificate_form
    }
    return render(request, 'student/student-edit.html', context)


logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)

@login_required(login_url='login')
def student_delete(request, reg_no):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    if user_profile.employee_type != 'professor':
        messages.error(request, "You do not have permission to delete this student please contact to Principal Sir ")
        return redirect('student-list')

    try:
        student = get_object_or_404(AcademicInfo, registration_no=reg_no)
        student.is_deleted = True
        student.save()
        messages.success(request, f"Student deleted successfully. <a href='{reverse('student-undo-delete', args=[student.registration_no])}'>Undo</a>")
        logger.info(f"Student with registration number {reg_no} marked as deleted by user {request.user}")
    except Exception as e:
        messages.error(request, f"Error deleting student: {e}")
        logger.error(f"Error deleting student with registration number {reg_no}: {e}")

    return redirect('student-list')





# def student_search(request):
#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

#     if user_profile.employee_type != 'professor':
#         return redirect('login')

#     forms = StudentSearchForm()
#     cls_name = request.GET.get('class_info', None)
#     reg_no = request.GET.get('registration_no', None)
    
#     if cls_name:
#         student = AcademicInfo.objects.filter(class_info=cls_name)
#         if reg_no:
#             student = student.filter(registration_no=reg_no)
#         context = {
#             'profile' : user_profile,
#             'forms': forms,
#             'student': student
#         }
#         return render(request, 'student/student-search.html', context)
#     else:
#         student = AcademicInfo.objects.filter(registration_no=reg_no)
#         context = {
#             'profile' : user_profile,
#             'forms': forms,
#             'student': student
#         }
#         return render(request, 'student/student-search.html', context)
#     context = {
#             'profile' : user_profile,
#             'forms': forms,
#             'student': student
#         }
#     return render(request, 'student/student-search.html', context)




def student_search(request,teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['teacher', 'professor']:
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)

    # Check if user is not a professor, redirect if necessary
    if user_profile.employee_type not in  ['teacher', 'professor']:
        return redirect('login')  # You should define your login URL here

    form = StudentSearchForm(request.GET or None)
    cls_name = request.GET.get('class_info', None)
    session_info = request.GET.get('session_info', None)
    reg_no = request.GET.get('registration_no', None)
    student_name = request.GET.get('name', None)
    student = AcademicInfo.objects.none()

    queries = Q()

    if reg_no:
        if not reg_no.isdigit():
            return redirect('/student/student-search/?error=invalid_registration_no')
        queries &= Q(registration_no=reg_no)

    if cls_name and session_info:  # Both cls_name and session_info are required
        queries &= Q(class_info=cls_name, session_info=session_info)
    
    
    if cls_name :  # Both cls_name and session_info are required
        queries &= Q(class_info=cls_name)

    if student_name:
        queries &= Q(personal_info__name__icontains=student_name)

    if queries:
        student = AcademicInfo.objects.filter(queries)

    context = {
        'teacher':teacher,
        'profile': user_profile,
        'form': form,
        'student': student
    }
    return render(request, 'student/student-search.html', context)
def enrolled_student(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor', 'teacher'])

    forms = EnrolledStudentForm(request.GET)  # Populate form with GET data
    cls = request.GET.get('class_name', None)
    status = request.GET.get('status', None)

    # Build the queryset
    student_query = AcademicInfo.objects.all()

    if cls:
        student_query = student_query.filter(class_info=cls)

    if status and status != '':
        student_query = student_query.filter(status=status)

    context = {
        'profile': user_profile,
        'forms': forms,
        'student': student_query
    }
    return render(request, 'student/enrolled.html', context)
def student_enrolled(request, reg):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor','teacher'])
        
    student = AcademicInfo.objects.get(registration_no=reg)
    forms = StudentEnrollForm()
    if request.method == 'POST':
        forms = StudentEnrollForm(request.POST)
        if forms.is_valid():
            roll = forms.cleaned_data['roll_no']
            class_name = forms.cleaned_data['class_name']
            EnrolledStudent.objects.create(class_name=class_name, student=student, roll=roll)
            student.status = 'enrolled'
            student.save()
            return redirect('enrolled-student-list')
    context = {
        'profile' : user_profile,
        'student': student,
        'forms': forms
    }
    return render(request, 'student/student-enrolled.html', context)



def enrolled_student_list(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor', 'teacher'])

    student = EnrolledStudent.objects.all()
    forms = SearchEnrolledStudentForm(request.GET or None)

    class_name = request.GET.get('reg_class', None)
    session_year = request.GET.get('session_year', None)
    roll = request.GET.get('roll_no', None)

    # Check if roll number is provided without class_name or session_year
    if roll and not (class_name and session_year):
        forms.add_error(None, 'Please provide both class and session year to search by roll number.')
    
    elif class_name and session_year:
        # Filter by class_name and session_year
        student = EnrolledStudent.objects.filter(class_name=class_name, session_year=session_year)

        # If roll number is also provided, further filter by roll number
        if roll:
            student = student.filter(roll=roll)  # Corrected 'roll_no' to 'roll'

    context = {
        'profile': user_profile,
        'forms': forms,
        'student': student
    }
    return render(request, 'student/enrolled-student-list.html', context)
