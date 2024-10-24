from django.db import models
import random

from academic.models import ClassInfo, ClassRegistration,Session,GuideTeacher, Department
from administration.models import Designation
from account.models import UserProfile
from address.models import District, Upazilla, Union
from account.models import UserProfile

class PersonalInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='student_personal_info') 
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student-photos/')
    blood_group_choice = (
        ('a+', 'A+'),
        ('o+', 'O+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
        ('a-', 'A-'),
        ('o-', 'O-'),
        ('b-', 'B-'),
        ('ab-', 'AB-')
    )
    blood_group = models.CharField(choices=blood_group_choice, max_length=5)
    date_of_birth = models.DateField()
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)
    birth_certificate_no = models.IntegerField()
    religion_choice = (
        
        ('Hindu', 'Hindu'),
        ('Buddh', 'Buddh'),
        ('Muslim', 'Muslim'),
        ('sikh', 'sikh'),
        ('Jain', 'Jain'),
        ('Christian','Christian'),
        ('Others', 'Others')
    )
    religion = models.CharField(choices=religion_choice, max_length=45)
    nationality_choice = (
        ('Indian', 'Indian'),
        ('Others', 'Others')
    )
    nationality = models.CharField(choices=nationality_choice, max_length=45)

    def __str__(self):
        return self.name

class StudentAddressInfo(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE)
    union = models.ForeignKey(Union, on_delete=models.CASCADE)
    village = models.TextField()

    def __str__(self):
        return self.village


class GuardianInfo(models.Model):
    father_name = models.CharField(max_length=100)
    father_phone_no = models.CharField(max_length=11)
    father_occupation_choice = (
        ('Agriculture', 'Agriculture'),
        ('Banker', 'Banker'),
        ('Business', 'Business'),
        ('Doctor', 'Doctor'),
        ('Farmer', 'Farmer'),
        ('Fisherman', 'Fisherman'),
        ('Public Service', 'Public Service'),
        ('Private Service', 'Private Service'),
        ('Shopkeeper', 'Shopkeeper'),
        ('Driver', 'Driver'),
        ('Worker', 'Worker'),
        ('N/A', 'N/A'),
    )
    father_occupation = models.CharField(choices=father_occupation_choice, max_length=45)
    father_yearly_income = models.IntegerField()
    mother_name = models.CharField(max_length=100)
    mother_phone_no = models.CharField(max_length=11)
    mother_occupation_choice = (
        ('Agriculture', 'Agriculture'),
        ('Banker', 'Banker'),
        ('Business', 'Business'),
        ('Doctor', 'Doctor'),
        ('Farmer', 'Farmer'),
        ('Fisherman', 'Fisherman'),
        ('Public Service', 'Public Service'),
        ('Private Service', 'Private Service'),
        ('Shopkeeper', 'Shopkeeper'),
        ('Driver', 'Driver'),
        ('Worker', 'Worker'),
        ('N/A', 'N/A'),
    )
    mother_occupation = models.CharField(choices=mother_occupation_choice, max_length=45)
    guardian_name = models.CharField(max_length=100)
    guardian_phone_no = models.CharField(max_length=11)
    guardian_email = models.EmailField(blank=True, null=True)
    relationship_choice = (
        ('Teacher', 'Teacher'),
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
        ('Other','Other')
    )
    relationship_with_student = models.CharField(choices=relationship_choice, max_length=45)

    def __str__(self):
        return self.guardian_name

class EmergencyContactDetails(models.Model):
    emergency_guardian_name = models.CharField(max_length=100)
    address = models.TextField()
    relationship_choice = (
        ('Teacher', 'Teacher'),
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),\
        ('Other','Other')
    )
    relationship_with_student = models.CharField(choices=relationship_choice, max_length=45)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.emergency_guardian_name

class PreviousAcademicInfo(models.Model):
    institute_name = models.CharField(max_length=100)
    name_of_exam = models.CharField(max_length=100)
    group = models.CharField(max_length=45)
    gpa = models.CharField(max_length=10)
    board_roll = models.IntegerField()
    passing_year = models.IntegerField()

    def __str__(self):
        return self.institute_name

class PreviousAcademicCertificate(models.Model):
    birth_certificate = models.FileField(upload_to='documents/', blank=True)
    release_letter = models.FileField(upload_to='documents/', blank=True)
    testimonial = models.FileField(upload_to='documents/', blank=True)
    marksheet = models.FileField(upload_to='documents/', blank=True)
    stipen_certificate = models.FileField(upload_to='documents/', blank=True)
    other_certificate = models.FileField(upload_to='documents/', blank=True)

class AcademicInfo(models.Model):
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    session_info = models.ForeignKey(Session, on_delete=models.CASCADE )
    class_teacher = models.ForeignKey(GuideTeacher, on_delete=models.CASCADE )
    administration = models.ForeignKey(Designation,on_delete=models.CASCADE)
    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE , null=True)
    registration_no = models.IntegerField(unique=True, default=random.randint(000000, 999999))
    status_select = (
        ('not enroll', 'Not Enroll'),
        ('enrolled', 'Enrolled'),
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('passed', 'Passed'),
    )
    status = models.CharField(choices=status_select, default='not enroll', max_length=15)
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
    address_info = models.ForeignKey(StudentAddressInfo, on_delete=models.CASCADE, null=True)
    guardian_info = models.ForeignKey(GuardianInfo, on_delete=models.CASCADE, null=True)
    emergency_contact_info = models.ForeignKey(EmergencyContactDetails, on_delete=models.CASCADE, null=True)
    previous_academic_info = models.ForeignKey(PreviousAcademicInfo, on_delete=models.CASCADE, null=True)
    previous_academic_certificate = models.ForeignKey(PreviousAcademicCertificate, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.registration_no)

class EnrolledStudent(models.Model):
    class_name = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    student = models.OneToOneField(AcademicInfo, on_delete=models.CASCADE)
    roll = models.IntegerField()
    session_year = models.ForeignKey(Session, default=1, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['class_name', 'session_year','roll']
    
    def __str__(self):
        return f"{self.student} enrolled in {self.class_name} for {self.session_year}"
