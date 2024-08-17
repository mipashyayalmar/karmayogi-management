from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import UserProfile
from .forms import SearchEnrolledStudentForm
from student.models import EnrolledStudent
from academic.models import ClassRegistration
from .models import StudentAttendance

def student_attendance(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, employee_type='professor')

    if user_profile.employee_type != 'professor':
        return redirect('login')

    forms = SearchEnrolledStudentForm()
    class_name = request.GET.get('reg_class', None)
    if class_name:
        class_info = ClassRegistration.objects.get(id=class_name)
        student = EnrolledStudent.objects.filter(class_name=class_name)
        context = {
            'profile' : user_profile,
            'forms': forms,
            'student': student,
            'class_info': class_info
        }
        return render(request, 'attendance/student-attendance.html', context)
    context = {
        'profile' : user_profile,
        'forms': forms,
        
    }
    return render(request, 'attendance/student-attendance.html', context)

class SetAttendance(APIView):
    def get(self, request, std_class, std_roll):
        try:
            StudentAttendance.objects.create_attendance(std_class, std_roll)
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)