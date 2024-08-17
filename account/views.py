from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout as auth_logout  # Rename logout
import student
import teacher
import employee
import academic
from .forms import AdminLoginForm, ProfileForm
from django.contrib import messages
from django.conf.urls import handler404


def login_home(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect them to their respective page
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.employee_type == 'professor':
            return redirect('professor_profiles')  # Redirect to professor profile page
        elif user_profile.employee_type == 'teacher':
            return redirect('teacher_profiles')  # Redirect to teacher profile page
        elif user_profile.employee_type == 'student':
            return redirect('student_profiles')  # Redirect to student profile page
        elif user_profile.employee_type == 'registrar':
            return redirect('registrar_profiles')  # Redirect to registrar profile page
        else:
            return redirect('login')  # Redirect to the home page for other employees

    forms = AdminLoginForm()
    if request.method == 'POST':
        forms = AdminLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    if user_profile.employee_type == 'professor':
                        return redirect('professor_profiles')  # Redirect to professor profile page
                    elif user_profile.employee_type == 'teacher':
                        return redirect('teacher_profiles')  # Redirect to teacher profile page
                    elif user_profile.employee_type == 'student':
                        return redirect('student_profiles')  # Redirect to student profile page
                    elif user_profile.employee_type == 'registrar':
                        return redirect('registrar_profiles')  # Redirect to registrar profile page
                    else:
                        return redirect('home')  # Redirect to the home page for other employees
                except UserProfile.DoesNotExist:
                    pass  # Handle the case where the user profile does not exist
    context = {'forms': forms}
    return render(request, 'administration/login.html', context)

def logout(request):
    auth_logout(request)  # Call Django's logout function
    return redirect('login')




# def custom_page_not_found_view(request, exception):
#     return redirect('/login')

# handler404 = custom_page_not_found_view


@login_required(login_url='login')
def home_page(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor','teacher'])

    # if user_profile.employee_type != 'professor':
    #     return redirect('login') 
    total_student = student.models.AcademicInfo.objects.count()
    total_teacher = teacher.models.PersonalInfo.objects.count()
    total_employee = employee.models.PersonalInfo.objects.count()
    total_class = academic.models.ClassRegistration.objects.count()
    context = {
        'student': total_student,
        'teacher': total_teacher,
        'employee': total_employee,
        'total_class': total_class,
        'profile' : user_profile,
        
    }
    return render(request, 'professor/home', context)

@login_required
def profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        return redirect('profile')  
    context = {
        'profile': profile
    }
    return render(request, 'account/profile.html', context)



@login_required
def update_profile_2(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        return redirect('profile')  
    context = {
        'profile': profile
    }
    return render(request, 'account/profile.html', context)


@login_required
def update_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        messages.info(request, "Please update your profile information.")
        return redirect('update_profile_2')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
        else:
            print(form.errors)  # Debugging: print form errors to the console
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'account/update-profile.html', context)


