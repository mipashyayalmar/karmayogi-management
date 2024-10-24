from django.db import models
from address.models import District, Upazilla, Union
from administration.models import Designation
from academic.models import Department
from account.models import UserProfile


class EmployeeAddressInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE, null=True)
    union = models.ForeignKey(Union, on_delete=models.CASCADE, null=True)
    village = models.TextField()

    def __str__(self):
        return self.village


class EducationInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    name_of_exam = models.CharField(max_length=100)
    institute = models.CharField(max_length=255)
    group = models.CharField(max_length=100)
    grade = models.CharField(max_length=45)
    board = models.CharField(max_length=45)
    passing_year = models.IntegerField()

    def __str__(self):
        return self.name_of_exam


class TrainingInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    training_name = models.CharField(max_length=100)
    year = models.IntegerField()
    duration = models.IntegerField()
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.training_name


class EmployeeJobInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category_choice = (
        ('engineering', 'Engineering'),
        ('bcs', 'BCS'),
        ('nationalized', 'Nationalized'),
        ('10% quota', '10% quota'),
        ('non govt.', 'Non Govt.'),
    )
    category = models.CharField(choices=category_choice, max_length=45)
    joining_date = models.DateField()
    institute_name = models.CharField(max_length=100)
    job_designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    scale = models.IntegerField()
    grade_of_post = models.CharField(max_length=45)
    first_time_scale_due_year = models.IntegerField()
    second_time_scale_due_year = models.IntegerField()
    promotion_due_year = models.IntegerField()
    recreation_leave_due_year = models.IntegerField()
    expected_retirement_year = models.IntegerField()

    def __str__(self):
        return self.institute_name


class ExperienceInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    institute_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=45)
    trainer = models.CharField(max_length=45)

    def __str__(self):
        return self.institute_name


class PersonalInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=45)
    photo = models.ImageField()
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=45)
    nationality = models.CharField(max_length=45)
    religion = models.CharField(max_length=45)
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    blood_group_choice = (
        ('a+', 'A+'),
        ('o+', 'O+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
        ('a-', 'A-'),
        ('o-', 'O-'),
        ('b-', 'B-'),
        ('ab-', 'AB-'),
    )
    blood_group = models.CharField(choices=blood_group_choice, max_length=5)
    e_tin = models.IntegerField(unique=True)
    nid = models.IntegerField(unique=True)
    driving_license_passport = models.IntegerField(unique=True)
    phone_no = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=255, unique=True)
    father_name = models.CharField(max_length=45)
    mother_name = models.CharField(max_length=45)
    marital_status_choice = (
        ('married', 'Married'),
        ('single', 'Single'),
    )
    marital_status = models.CharField(choices=marital_status_choice, max_length=10)
    address = models.ForeignKey(EmployeeAddressInfo, on_delete=models.CASCADE, null=True)
    education = models.ForeignKey(EducationInfo, on_delete=models.CASCADE, null=True)
    training = models.ForeignKey(TrainingInfo, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(EmployeeJobInfo, on_delete=models.CASCADE, null=True)
    experience = models.ForeignKey(ExperienceInfo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the PersonalInfo instance first
        
        # Populate userprofile in related models
        if self.userprofile:
            # Update related models with the UserProfile
            self.address.userprofile = self.userprofile
            self.address.save()
            self.education.userprofile = self.userprofile
            self.education.save()
            self.training.userprofile = self.userprofile
            self.training.save()
            self.job.userprofile = self.userprofile
            self.job.save()
            self.experience.userprofile = self.userprofile
            self.experience.save()