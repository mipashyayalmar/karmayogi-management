from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import UserProfile
from .forms import SearchEnrolledStudentForm
from student.models import EnrolledStudent
from academic.models import ClassRegistration, Session
from .models import StudentAttendance
from .forms import AttendanceForm
from .models import AttendanceManager

def student_attendance(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    if user_profile.employee_type != 'professor':
        return redirect('login')

    forms = SearchEnrolledStudentForm()
    class_name = request.GET.get('reg_class', None)
    session_year = request.GET.get('session', None)  
    students = EnrolledStudent.objects.none() 
    if class_name and session_year:
        class_info = ClassRegistration.objects.get(id=class_name)
        students = EnrolledStudent.objects.filter(class_name=class_info, session_year=session_year) 
    context = {
        'profile': user_profile,
        'forms': forms,
        'student': students,  # Pass the filtered students to the template
        'class_info': class_info if class_name else None,
    }
    
    return render(request, 'attendance/student-attendance.html', context)

class SetAttendance(APIView):
    def get(self, request, std_class, std_roll):
        try:
            StudentAttendance.objects.create_attendance(std_class, std_roll)
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'Failed', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
def add_attendance(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    # Allow only professors to add attendance
    if user_profile.employee_type != 'professor':
        return redirect('login')

    class_id = request.GET.get('class_id')
    students = None
    selected_class = None
    if class_id:
        selected_class = ClassRegistration.objects.get(id=class_id)
        students = EnrolledStudent.objects.filter(class_name=selected_class)

    form = AttendanceForm(class_id=class_id)

    if request.method == "POST":
        form = AttendanceForm(request.POST, class_id=request.POST.get('select_class'))
        if form.is_valid():
            class_name = form.cleaned_data['select_class']
            student_roll = form.cleaned_data['student_roll']
            subject = form.cleaned_data['subject']

            try:
                AttendanceManager().create_attendance(class_name.name, student_roll, subject)
                message = "Attendance added successfully!"
            except Exception as e:
                message = f"Error: {str(e)}"
            return render(request, 'attendance/add_attendance.html', {
                'form': form,
                'profile': user_profile,  # Pass user_profile for the sidebar
                'message': message,
                'classes': ClassRegistration.objects.all(),
                'students': students,
                'selected_class': selected_class
            })

    return render(request, 'attendance/add_attendance.html', {
        'form': form,
        'profile': user_profile,  # Pass user_profile for the sidebar
        'classes': ClassRegistration.objects.all(),
        'students': students,
        'selected_class': selected_class
    })
