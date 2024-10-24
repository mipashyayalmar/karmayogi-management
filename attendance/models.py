# attendance/models.py

from django.db import models
from academic.models import ClassRegistration
from student.models import EnrolledStudent
from result.models import SubjectRegistration

class AttendanceManager(models.Manager):
    def create_attendance(self, std_class, std_roll, subject):
        std_cls = ClassRegistration.objects.get(name=std_class)
        std = EnrolledStudent.objects.get(roll=std_roll, class_name=std_cls)
        std_att = StudentAttendance.objects.create(
            select_class=std_cls,
            student=std,
            subject=subject,
            status=1
        )
        return std_att

class StudentAttendance(models.Model):
    select_class = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectRegistration, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    objects = AttendanceManager()

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.student.personal_info.name} - {self.subject.subject_name}"
