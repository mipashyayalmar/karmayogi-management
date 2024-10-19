from django.shortcuts import render, redirect, get_object_or_404
from account.models import UserProfile
from academic.models import ClassRegistration
from .forms import SubjectRegistrationForm, ClassSelectMarkEntryForm, ClassSelectSubjectListForm
from student.models import AcademicInfo
from .models import SubjectRegistration

def add_subject(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    # Allow access to both professors and teachers
    if user_profile.employee_type not in ['professor', 'teacher']:
        return redirect('login')

    if request.method == 'POST':
        subject_form = SubjectRegistrationForm(request.POST, request.FILES)
        if subject_form.is_valid():
            subject_form.save()
            return redirect('subject-list')
    else:
        subject_form = SubjectRegistrationForm()

    context = {
        'subject_form': subject_form,
        'profile': user_profile,
    }

    return render(request, 'result/add-subject.html', context)
    
def subject_list(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor', 'teacher'])

    # No specific permission check here; all teachers and professors can access the list
    form = ClassSelectSubjectListForm(request.GET or None)
    select_class = request.GET.get('select_class', None)
    subjects = SubjectRegistration.objects.none()  # Initialize subjects

    if select_class:
        cls = get_object_or_404(ClassRegistration, id=select_class)
        subjects = SubjectRegistration.objects.filter(select_class=cls)

    context = {
        'profile': user_profile,
        'form': form,
        'subjects': subjects,
    }
    return render(request, 'result/subject-list.html', context)

def subject_detail(request, pk):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor', 'teacher'])

    # Allow access to both professors and teachers
    if user_profile.employee_type not in ['professor', 'teacher']:
        return redirect('login')

    subject = get_object_or_404(SubjectRegistration, pk=pk)
    return render(request, 'result/subject_detail.html', {
        'subject': subject,
        'profile': user_profile,
    })

def mark_entry(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    # Allow access to both professors and teachers
    if user_profile.employee_type not in ['professor', 'teacher']:
        return redirect('login')

    form = ClassSelectMarkEntryForm(request.GET or None)
    select_class_id = request.GET.get('select_class', None)
    students = AcademicInfo.objects.none()

    if select_class_id:
        try:
            cls = get_object_or_404(ClassRegistration, id=select_class_id)
            students = AcademicInfo.objects.filter(class_info=cls)
        except (ValueError, ClassRegistration.DoesNotExist):
            return render(request, 'result/mark-entry.html', {
                'profile': user_profile,
                'form': form,
                'error': 'Invalid class selected.'
            })

    context = {
        'profile': user_profile,
        'form': form,
        'students': students
    }
    return render(request, 'result/mark-entry.html', context)

def mark_table(request, subject):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    # Allow access to both professors and teachers
    if user_profile.employee_type not in ['professor', 'teacher']:
        return redirect('login')

    return render(request, 'result/mark-table.html')
