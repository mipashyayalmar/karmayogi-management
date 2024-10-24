from django.contrib import admin
from .models import (
    EmployeeAddressInfo, EducationInfo, TrainingInfo, 
    EmployeeJobInfo, ExperienceInfo, PersonalInfo
)
from account.models import UserProfile  # Import UserProfile for related usage


# Admin classes with UserProfile as the first column

class EmployeeAddressInfoAdmin(admin.ModelAdmin):
    list_display = ['get_userprofile', 'district', 'upazilla', 'union', 'village']
    search_fields = ['village', 'userprofile__user__username']

    def get_userprofile(self, obj):
        return obj.userprofile  # Displays UserProfile in the first column
    get_userprofile.short_description = 'User Profile'  # Column header


class EducationInfoAdmin(admin.ModelAdmin):
    list_display = ['get_userprofile', 'name_of_exam', 'institute', 'group', 'grade', 'board', 'passing_year']
    search_fields = ['name_of_exam', 'institute', 'userprofile__user__username']
    list_filter = ['board', 'passing_year']

    def get_userprofile(self, obj):
        return obj.userprofile
    get_userprofile.short_description = 'User Profile'


class TrainingInfoAdmin(admin.ModelAdmin):
    list_display = ['get_userprofile', 'training_name', 'year', 'duration', 'place']
    search_fields = ['training_name', 'place', 'userprofile__user__username']
    list_filter = ['year']

    def get_userprofile(self, obj):
        return obj.userprofile
    get_userprofile.short_description = 'User Profile'


class EmployeeJobInfoAdmin(admin.ModelAdmin):
    list_display = ['get_userprofile', 'category', 'joining_date', 'institute_name', 'job_designation', 'department']
    search_fields = ['institute_name', 'userprofile__user__username']
    list_filter = ['category', 'joining_date']

    def get_userprofile(self, obj):
        return obj.userprofile
    get_userprofile.short_description = 'User Profile'


class ExperienceInfoAdmin(admin.ModelAdmin):
    list_display = ['get_userprofile', 'institute_name', 'designation', 'trainer']
    search_fields = ['institute_name', 'designation', 'userprofile__user__username']

    def get_userprofile(self, obj):
        return obj.userprofile
    get_userprofile.short_description = 'User Profile'


class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['get_userprofile', 'name', 'phone_no', 'email', 'gender', 'marital_status', 'date_of_birth']
    search_fields = ['name', 'phone_no', 'email', 'userprofile__user__username']
    list_filter = ['gender', 'marital_status', 'blood_group']

    fieldsets = (
        (None, {
            'fields': ('userprofile', 'name', 'photo', 'date_of_birth', 'place_of_birth', 
                       'nationality', 'religion', 'gender', 'blood_group')
        }),
        ('Contact Details', {
            'fields': ('phone_no', 'email', 'e_tin', 'nid', 'driving_license_passport')
        }),
        ('Family Details', {
            'fields': ('father_name', 'mother_name', 'marital_status')
        }),
        ('Related Info', {
            'fields': ('address', 'education', 'training', 'job', 'experience')
        }),
    )

    def get_userprofile(self, obj):
        return obj.userprofile
    get_userprofile.short_description = 'User Profile'


# Register all models with their respective Admin classes
admin.site.register(EmployeeAddressInfo, EmployeeAddressInfoAdmin)
admin.site.register(EducationInfo, EducationInfoAdmin)
admin.site.register(TrainingInfo, TrainingInfoAdmin)
admin.site.register(EmployeeJobInfo, EmployeeJobInfoAdmin)
admin.site.register(ExperienceInfo, ExperienceInfoAdmin)
admin.site.register(PersonalInfo, PersonalInfoAdmin)
