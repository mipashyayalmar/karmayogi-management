from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import District, Upazilla, Union, PersonalInfo
from account.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import logging
from django.http import HttpResponseForbidden

from teacher.models import PersonalInfo as TeacherPersonalInfo

@login_required(login_url='login')
def load_upazilla(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        district_id = request.GET.get('district')
        upazilla = Upazilla.objects.filter(district_id=district_id).order_by('name')
        upazilla_id = request.GET.get('upazilla')
        union = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
        context = {
            'upazilla': upazilla,
            'union': union,
            'profile': user_profile
        }
        return render(request, 'others/upazilla_dropdown_list_options.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def teacher_registration(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = forms.PersonalInfoForm()
        address_forms = forms.AddressInfoForm()
        education_form = forms.EducationInfoForm()
        training_form = forms.TrainingInfoForm()
        job_form = forms.JobInfoForm()
        experience_form = forms.ExperienceInfoForm()
        if request.method == 'POST':
            form = forms.PersonalInfoForm(request.POST, request.FILES)
            address_form = forms.AddressInfoForm(request.POST)
            education_form = forms.EducationInfoForm(request.POST)
            training_form = forms.TrainingInfoForm(request.POST)
            job_form = forms.JobInfoForm(request.POST)
            experience_form = forms.ExperienceInfoForm(request.POST)
            if form.is_valid() and address_form.is_valid() and education_form.is_valid() and training_form.is_valid() and job_form.is_valid() and experience_form.is_valid():
                address_info = address_form.save()
                education_info = education_form.save()
                training_info = training_form.save()
                job_info = job_form.save()
                experience_info = experience_form.save()
                personal_info = form.save(commit=False)
                personal_info.address = address_info
                personal_info.education = education_info
                personal_info.training = training_info
                personal_info.job = job_info
                personal_info.experience = experience_info
                personal_info.save()
                return redirect('teacher-list')
        context = {
            'form': form,
            'address_forms': address_forms,
            'education_form': education_form,
            'training_form': training_form,
            'job_form': job_form,
            'experience_form': experience_form,
            'profile': user_profile
        }
        return render(request, 'teacher/teacher-registration.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')


<<<<<<< HEAD
@login_required(login_url='login')
def teacher_list(request):
    # Get the logged-in user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.employee_type in ['teacher', 'professor']:
        if user_profile.employee_type == 'professor':
            # Professors can view all teachers
            teachers = TeacherPersonalInfo.objects.filter(is_delete=False)
            teacher_count = teachers.count()
        else:
            # Teachers can only view those in their department
            user_teacher_info = TeacherPersonalInfo.objects.filter(
                address__userprofile=user_profile
            ).first()

            if not user_teacher_info:
                return HttpResponseForbidden("Teacher information not found for this user.")

            teacher_department = user_teacher_info.job.department

            teachers = TeacherPersonalInfo.objects.filter(
                job__department=teacher_department, is_delete=False
            )
            teacher_count = teachers.count()

        context = {
            'teachers': teachers,
            'teacher_count': teacher_count,
            'profile': user_profile,
        }
        return render(request, 'teacher/teacher-list.html', context)

    return HttpResponseForbidden("You do not have permission to view this page.")

=======


@login_required(login_url='login')
def teacher_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the user is a teacher or professor
    if user_profile.employee_type in ['teacher', 'professor']:
        # Get all teachers' personal info
        teacher = PersonalInfo.objects.all()
        context = {
            'teacher': teacher,
            'profile': user_profile
        }
        return render(request, 'teacher/teacher-list.html', context)
    else:
        # Return a forbidden response if the user is not a teacher or professor
        return HttpResponseForbidden("You do not have permission to view this page.")
>>>>>>> 29f2085b916bc7ee9553cfc80f3870a0d2da48b6

@login_required(login_url='login')
def teacher_profile(request, teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Check if user is teacher or professor
    if user_profile.employee_type in ['teacher', 'professor']:
        # Get the teacher related to the user profile if no teacher_id is provided
        if not teacher_id:
            teacher = get_object_or_404(PersonalInfo, address__userprofile=user_profile)
            teacher_id = teacher.id
        else:
            teacher = get_object_or_404(PersonalInfo, id=teacher_id)
        
        # Check if teacher's address userprofile matches the logged-in user profile
        if teacher.address.userprofile == user_profile:
            context = {
                'teacher': teacher,
                'profile': user_profile
            }
            return render(request, 'account/profile.html', context)
        else:
            context = {
                'teacher': teacher,
                'profile': user_profile
            }
            return render(request, 'teacher/teacher-profile.html', context)
    else:
        return HttpResponseForbidden("You do not have permission to view this page.")





logger = logging.getLogger(__name__)
@login_required(login_url='login')
def teacher_delete(request, teacher_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        try:
            teacher = get_object_or_404(PersonalInfo, id=teacher_id)
            teacher.delete()
            messages.success(request, "Teacher deleted successfully.")
            logger.info(f"Teacher with id {teacher_id} deleted successfully by user {request.user}")
        except Exception as e:
            messages.error(request, f"Error deleting teacher: {e}")
            logger.error(f"Error deleting teacher with id {teacher_id}: {e}")
        return redirect('teacher-list')
    else:
        messages.error(request, "You do not have permission to delete this teacher.")
        return redirect('some_other_page_or_show_error_message')


@login_required(login_url='login')
def teacher_edit(request, teacher_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type in ['teacher', 'professor']:
        teacher = PersonalInfo.objects.get(id=teacher_id)
        form = forms.PersonalInfoForm(instance=teacher)
        address_form = forms.AddressInfoForm(instance=teacher.address)
        education_form = forms.EducationInfoForm(instance=teacher.education)
        training_form = forms.TrainingInfoForm(instance=teacher.training)
        job_form = forms.JobInfoForm(instance=teacher.job)
        experience_form = forms.ExperienceInfoForm(instance=teacher.experience)
        
        if request.method == 'POST':
            form = forms.PersonalInfoForm(request.POST, request.FILES, instance=teacher)
            address_form = forms.AddressInfoForm(request.POST, instance=teacher.address)
            education_form = forms.EducationInfoForm(request.POST, instance=teacher.education)
            training_form = forms.TrainingInfoForm(request.POST, instance=teacher.training)
            job_form = forms.JobInfoForm(request.POST, instance=teacher.job)
            experience_form = forms.ExperienceInfoForm(request.POST, instance=teacher.experience)
            
            if (form.is_valid() and address_form.is_valid() and education_form.is_valid() and
                training_form.is_valid() and job_form.is_valid() and experience_form.is_valid()):
                address_info = address_form.save()
                education_info = education_form.save()
                training_info = training_form.save()
                job_info = job_form.save()
                experience_info = experience_form.save()
                
                personal_info = form.save(commit=False)
                personal_info.address = address_info
                personal_info.education = education_info
                personal_info.training = training_info
                personal_info.job = job_info
                personal_info.experience = experience_info
                personal_info.save()
                
                return redirect('/')
        
        context = {
            'form': form,
            'address_form': address_form,
            'education_form': education_form,
            'training_form': training_form,
            'job_form': job_form,
            'experience_form': experience_form,
            'profile': user_profile
        }
        return render(request, 'teacher/teacher-edit.html', context)
    else:
        return HttpResponseForbidden("You do not have permission to edit this teacher.")
