from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from academic.models import ClassRegistration
from account.models import UserProfile

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
        classes = ClassInfo.objects.all()
        context = {'form': form, 'classes': classes, 'profile': user_profile}
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
    if user_profile.employee_type == 'professor':
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
def class_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        registered_classes = ClassRegistration.objects.all()
        context = {'registered_classes': registered_classes, 'profile': user_profile}
        return render(request, 'academic/class-list.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def create_guide_teacher(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
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

@login_required(login_url='login')
def add_district(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = DistrictForm()
        if request.method == 'POST':
            form = DistrictForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('district')
        districts = District.objects.all()
        context = {'form': form, 'districts': districts, 'profile': user_profile}
        return render(request, 'address/district.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def add_upazilla(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = UpazillaForm()
        if request.method == 'POST':
            form = UpazillaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('upazilla')
        upazillas = Upazilla.objects.all()
        context = {'form': form, 'upazillas': upazillas, 'profile': user_profile}
        return render(request, 'address/upazilla.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')

@login_required(login_url='login')
def add_union(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.employee_type == 'professor':
        form = UnionForm()
        if request.method == 'POST':
            form = UnionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('union')
        unions = Union.objects.all()
        context = {'form': form, 'unions': unions, 'profile': user_profile}
        return render(request, 'address/union.html', context)
    else:
        return redirect('some_other_page_or_show_error_message')
