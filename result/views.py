from django.shortcuts import render, redirect, get_object_or_404
from account.models import UserProfile
from academic.models import ClassRegistration
from .forms import SubjectRegistrationForm, ClassSelectMarkEntryForm, ClassSelectSubjectListForm
from student.models import AcademicInfo
from .models import SubjectRegistration
from .forms import SubjectRegistrationForm



def add_subject(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    if user_profile.employee_type != 'professor':
        return redirect('login')

    if request.method == 'POST':
        subject_form = SubjectRegistrationForm(request.POST, request.FILES)  # Ensure request.FILES is included
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
        user_profile = UserProfile.objects.create(user=request.user, employee_type=['professor','teacher'])

    # if user_profile.employee_type != 'professor':
    #     return redirect('login')

    form = ClassSelectSubjectListForm(request.GET or None)
    select_class = request.GET.get('select_class', None)
    if select_class:
        cls = ClassRegistration.objects.get(id=select_class)
        subjects = SubjectRegistration.objects.filter(select_class=cls)
        context = {
            'profile' : user_profile,
            'form': form,
            'subjects': subjects}
        return render(request, 'result/subject-list.html', context)

    context = {
        'profile' : user_profile,
        'form': form}
    return render(request, 'result/subject-list.html', context)



def subject_detail(request, pk):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

        if user_profile.employee_type != 'professor':
            return redirect('login')

        subject = get_object_or_404(SubjectRegistration, pk=pk)
        return render(request, 'result/subject_detail.html', {
            'subject': subject,
            'profile' : user_profile,
        })


# def mark_entry(request):
#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

#     if user_profile.employee_type != 'professor':
#         return redirect('login')

#     form = ClassSelectMarkEntryForm(request.GET or None)
#     select_class = request.GET.get('select_class', None)
#     if select_class:
#         cls = ClassRegistration.objects.get(id=select_class)
#         student = AcademicInfo.objects.filter(class_info=cls)
#         context = {'profile' : user_profile,
#                   'form': form, 
#                   'student': student,
#                   }
#         return render(request, 'result/mark-entry.html', context)
#     context = {'profile' : user_profile,'form': form}
#     return render(request, 'result/mark-entry.html', context)




def mark_entry(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    if user_profile.employee_type != 'professor':
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

    if user_profile.employee_type != 'professor':
        return redirect('login')

    return render(request, 'result/mark-table.html')
