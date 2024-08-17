from django import forms

from .models import *
from academic.models import ClassInfo

class AcademicInfoForm(forms.ModelForm):
    class Meta:
        model = AcademicInfo
        exclude = ['registration_no', 'status', 'personal_info', 'address_info', 'guardian_info', 'emergency_contact_info', 'previous_academic_info', 'previous_academic_certificate', 'is_delete']
        widgets = {
            'class_info': forms.Select(attrs={'class': 'form-control'}),
            'session_info':forms.Select(attrs={'class': 'form-control'}),
            'class_teacher':forms.Select(attrs={'class': 'form-control'}),
            'administration':forms.Select(attrs={'class':'form-control'}),
            'userprofile':forms.Select(attrs={'class': 'form-control'}),
            # 'department'  : forms.Select(attrs={'class': 'form-control'})
        } 
    def __init__(self, *args, **kwargs):
            super(AcademicInfoForm, self).__init__(*args, **kwargs)
            self.fields['class_info'].label = 'Select Class  '
            self.fields['session_info'].label = 'Academic Year '

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control','type':'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_certificate_no': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'})
        }

class StudentAddressInfoForm(forms.ModelForm):
    class Meta:
        model = StudentAddressInfo
        fields = '__all__'
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control'}),
            'upazilla': forms.Select(attrs={'class': 'form-control'}),
            'union': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'})
        }

    # union to village

    def __init__(self, *args, **kwargs):
        super(StudentAddressInfoForm, self).__init__(*args, **kwargs)
        self.fields['union'].label = 'Village'
        self.fields['village'].label = 'House NO/Street/Landmark  With  Pin Code'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['upazilla'].queryset = models.Upazilla.objects.none()

            if 'upazilla' in self.data:
                try:
                    district_id = int(self.data.get('district'))
                    self.fields['upazilla'].queryset = models.Upazilla.objects.filter(district_id=district_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['upazilla'].queryset = self.instance.district.upazilla_set.order_by('name')

            self.fields['union'].queryset = models.Union.objects.none()
        

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['upazilla'].queryset = Upazilla.objects.none()

            if 'upazilla' in self.data:
                try:
                    district_id = int(self.data.get('district'))
                    self.fields['upazilla'].queryset = Upazilla.objects.filter(district_id=district_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['upazilla'].queryset = self.instance.district.upazilla_set.order_by('name')

            self.fields['union'].queryset = Union.objects.none()

            if 'union' in self.data:
                try:
                    upazilla_id = int(self.data.get('upazilla'))
                    self.fields['union'].queryset = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['union'].queryset = self.instance.upazilla.union_set.order_by('name')


class GuardianInfoForm(forms.ModelForm):
    class Meta:
        model = GuardianInfo
        fields = '__all__'
        widgets = {
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.Select(attrs={'class': 'form-control'}),
            'father_yearly_income': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.Select(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship_with_student': forms.Select(attrs={'class': 'form-control'}),
        }

class EmergencyContactDetailsForm(forms.ModelForm):
    class Meta:
        model = EmergencyContactDetails
        fields = '__all__'
        widgets = {
            'emergency_guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'relationship_with_student': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PreviousAcademicInfoForm(forms.ModelForm):
    class Meta:
        model = PreviousAcademicInfo
        fields = '__all__'
        widgets = {
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_of_exam': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.TextInput(attrs={'class': 'form-control'}),
            'board_roll': forms.TextInput(attrs={'class': 'form-control'}),
            'passing_year': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PreviousAcademicCertificateForm(forms.ModelForm):
    class Meta:
        model = PreviousAcademicCertificate
        fields = '__all__'


class StudentSearchForm(forms.Form):
    session_info = forms.ModelChoiceField(required=False, queryset=Session.objects.all())
    class_info = forms.ModelChoiceField(required=False, queryset=ClassInfo.objects.all())
    registration_no = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Registration No', 'aria-controls': 'DataTables_Table_0'}))
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))




class StudentSearchForm(forms.Form):
    session_info = forms.ModelChoiceField(required=False, queryset=Session.objects.all())
    class_info = forms.ModelChoiceField(required=False, queryset=ClassInfo.objects.all())
    registration_no = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Registration No', 'aria-controls': 'DataTables_Table_0'}))
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by Name',
            'class': 'form-control'
        })
    )
  

from django import forms
from .models import ClassInfo

class EnrolledStudentForm(forms.Form):
    class_name = forms.ModelChoiceField(queryset=ClassInfo.objects.all())
    status_select = (
        ('', 'Any Status'),  # Added an empty option for any status
        ('not enroll', 'Not Enroll'),
        ('enrolled', 'Enrolled'),
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('passed', 'Passed'),
    )
    status = forms.ChoiceField(choices=status_select, required=False)



    def filter_students(self):
        status = self.cleaned_data.get('status')

        students = Student.objects.filter(class_registration=reg_class)

        if status:
            students = students.filter(status=status)


        return students

class StudentEnrollForm(forms.Form):
    class_name = forms.ModelChoiceField(queryset=ClassRegistration.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    roll_no = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Roll', 'class': 'form-control'}))

class SearchEnrolledStudentForm(forms.Form):
    reg_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all())
    roll_no = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Enter Roll'}))
   