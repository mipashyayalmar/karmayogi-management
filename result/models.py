from django.db import models
from academic.models import ClassInfo, ClassRegistration, Session, GuideTeacher, Department
from account.models import UserProfile

class SubjectRegistration(models.Model):
    select_class = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE, null=True)
    session_info = models.ForeignKey(Session, on_delete=models.CASCADE, default=1)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    subject_name = models.CharField(max_length=45)
    subject_code = models.IntegerField(unique=True)
    marks = models.IntegerField()
    pass_mark = models.IntegerField()
    add_date = models.DateField(auto_now_add=True)
    syllabus_picture = models.ImageField(upload_to='syllabus_pictures/', null=True, blank=True)

    def __str__(self):
        return self.subject_name
