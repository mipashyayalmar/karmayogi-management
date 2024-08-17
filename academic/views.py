from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from academic.models import ClassRegistration
from account.models import UserProfile
from teacher.models import PersonalInfo as TeacherPersonalInfo

@login_required(login_url='login')
def add_department(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = DepartmentForm()
        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('add-department')
        departments = Department.objects.all()
        context = {'form': form, 'departments': departments, 'profile': user_profile}
        return render(request, 'academic/add-department.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')
@login_required(login_url='login')
def add_class(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = ClassForm()
        if request.method == 'POST':
            form = ClassForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('create-class')
        class_objs = ClassInfo.objects.all()  # Ensure this variable matches the template
        context = {
            'form': form,
            'class_objs': class_objs,
            'profile': user_profile
        }
        return render(request, 'academic/create-class.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def create_section(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = SectionForm()
        if request.method == 'POST':
            form = SectionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('create-section')
        sections = Section.objects.all()
        context = {'form': form, 'sections': sections, 'profile': user_profile}
        return render(request, 'academic/create-section.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def create_session(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = SessionForm()
        if request.method == 'POST':
            form = SessionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('create-session')
        sessions = Session.objects.all()
        context = {'form': form, 'sessions': sessions, 'profile': user_profile}
        return render(request, 'academic/create-session.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def create_shift(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = ShiftForm()
        if request.method == 'POST':
            form = ShiftForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('create-shift')
        shifts = Shift.objects.all()
        context = {'form': form, 'shifts': shifts, 'profile': user_profile}
        return render(request, 'academic/create-shift.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def class_registration(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type  in ['teacher', 'professor']:
        form = ClassRegistrationForm()
        if request.method == 'POST':
            form = ClassRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('class-list')
        context = {'form': form, 'profile': user_profile}
        return render(request, 'academic/class-registration.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')

def class_list(request, teacher_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.employee_type in ['teacher', 'professor']:
        if not teacher_id:
            teacher = get_object_or_404(TeacherPersonalInfo, address__userprofile=user_profile)
        else:
            teacher = get_object_or_404(TeacherPersonalInfo, id=teacher_id)

    if user_profile.employee_type in ['teacher', 'professor']:
        register_class = ClassRegistration.objects.all()
        context = {
            'teacher' : teacher,
            'register_class': register_class,
            'profile': user_profile}
        return render(request, 'academic/class-list.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')  # Adjust this as needed

        
@login_required(login_url='login')
def create_guide_teacher(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type in ['teacher', 'professor']:
        form = GuideTeacherForm()
        if request.method == 'POST':
            form = GuideTeacherForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('guide-teacher')
        guide_teachers = GuideTeacher.objects.all()
        context = {'form': form, 'guide_teachers': guide_teachers, 'profile': user_profile}
        return render(request, 'academic/create-guide-teacher.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')
