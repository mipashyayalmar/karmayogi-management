from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import District, Upazilla, Union, PersonalInfo
from account.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import logging
from django.http import HttpResponseForbidden
from employee.models import PersonalInfo as EmployeePersonalInfo
from teacher.models import PersonalInfo as TeacherPersonalInfo

@login_required(login_url='login')
def load_upazilla(request):
    user_profile = UserProfile.objects.get(user=request.user)
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

@login_required(login_url='login')
def employee_registration(request):
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
                personal_info = form.save()
                address_info = address_form.save(commit=False)
                address_info.address = personal_info
                address_info.save()
                education_info = education_form.save(commit=False)
                education_info.education = personal_info
                education_info.save()
                training_info = training_form.save(commit=False)
                training_info.training = personal_info
                training_info.save()
                job_info = job_form.save(commit=False)
                job_info.job = personal_info
                job_info.save()
                experience_info = experience_form.save(commit=False)
                experience_info.experience = personal_info
                experience_info.save()
                return redirect('employee-list')

        context = {
            'form': form,
            'address_forms': address_forms,
            'education_form': education_form,
            'training_form': training_form,
            'job_form': job_form,
            'experience_form': experience_form,
            'profile': user_profile
        }
        return render(request, 'employee/employee-registration.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def employee_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.employee_type in ['professor', 'teacher']:
        if user_profile.employee_type == 'teacher':
            teacher_info = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
            teacher_department = teacher_info.job.department
            employees = EmployeePersonalInfo.objects.filter(job__department=teacher_department)
        else:
            employees = EmployeePersonalInfo.objects.all()

        context = {
            'employees': employees,
            'profile': user_profile,
        }
        return render(request, 'employee/employee-list.html', context)

    return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def employee_profile(request, employee_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type in ['professor', 'teacher']:
        employee = PersonalInfo.objects.get(id=employee_id)
        context = {
            'employee': employee,
            'profile': user_profile
        }
        return render(request, 'employee/employee-profile.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

logger = logging.getLogger(__name__)

@login_required(login_url='login')
def employee_delete(request, employee_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type in ['professor', 'teacher']:
        try:
            employee = get_object_or_404(PersonalInfo, id=employee_id)
            employee.delete()
            messages.success(request, "Employee deleted successfully.")
            logger.info(f"Employee with id {employee_id} deleted successfully by user {request.user}")
        except Exception as e:
            messages.error(request, f"Error deleting employee: {e}")
            logger.error(f"Error deleting employee with id {employee_id}: {e}")
        return redirect('employee-list')
    else:
        messages.error(request, "You do not have permission to delete this employee.")
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def employee_edit(request, employee_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type in ['professor', 'teacher']:
        employee = PersonalInfo.objects.get(id=employee_id)
        form = forms.PersonalInfoForm(instance=employee)
        address_forms = forms.AddressInfoForm(instance=employee.address)
        education_form = forms.EducationInfoForm(instance=employee.education)
        training_form = forms.TrainingInfoForm(instance=employee.training)
        job_form = forms.JobInfoForm(instance=employee.job)
        experience_form = forms.ExperienceInfoForm(instance=employee.experience)
        if request.method == 'POST':
            form = forms.PersonalInfoForm(request.POST, request.FILES, instance=employee)
            address_form = forms.AddressInfoForm(request.POST, instance=employee.address)
            education_form = forms.EducationInfoForm(request.POST, instance=employee.education)
            training_form = forms.TrainingInfoForm(request.POST, instance=employee.training)
            job_form = forms.JobInfoForm(request.POST, instance=employee.job)
            experience_form = forms.ExperienceInfoForm(request.POST, instance=employee.experience)
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
                return redirect('employee-list')
        context = {
            'form': form,
            'address_form': address_forms,
            'education_form': education_form,
            'training_form': training_form,
            'job_form': job_form,
            'experience_form': experience_form,
            'profile': user_profile
        }
        return render(request, 'employee/employee-edit.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')
