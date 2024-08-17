from django.shortcuts import render, redirect
from teacher.models import Department, Designation
from .forms import AddDesignationForm
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
from account import professor_views

@login_required
def add_designation(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If the user profile doesn't exist, create one with employee_type 'professor'
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    if user_profile.employee_type in ['teacher', 'professor']:
        if request.method == 'POST':
            forms = AddDesignationForm(request.POST)
            if forms.is_valid():
                forms.save()
                return redirect('designation')
        else:
            forms = AddDesignationForm()

        designation = Designation.objects.all()
        context = {
            'forms': forms,
            'designation': designation,
            'profile': user_profile,
        }
        return render(request, 'administration/designation.html', context)
    else:
        # Redirect non-professors to another page or show an error message
        return redirect('some_other_page_or_show_error_message')  # Adjust this as needed
