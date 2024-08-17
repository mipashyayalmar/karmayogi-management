from django import forms
from . import models
from academic.models import Department


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = models.PersonalInfo
        exclude = {'address', 'education', 'training', 'job', 'experience', 'is_delete'}
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_type': forms.Select(attrs={'class': 'form-control'}),
            'administration': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'data-default-file': '{% static "src/img/man.png" %}'
            }),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'caste': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'e_tin': forms.TextInput(attrs={'class': 'form-control'}),
            'nid': forms.NumberInput(attrs={'class': 'form-control'}),
            'driving_license_passport': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),

        }
    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        self.fields['e_tin'].label = 'Pan Card'
        self.fields['nid'].label = 'Adhar Card'



class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = models.AddressInfo
        fields = ('userprofile','district', 'upazilla', 'union', 'village')
        widgets = {
            'userprofile': forms.Select(attrs={'class':'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'upazilla': forms.Select(attrs={'class': 'form-control'}),
            'union': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # union to village

    def __init__(self, *args, **kwargs):
        super(AddressInfoForm, self).__init__(*args, **kwargs)
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

            if 'union' in self.data:
                try:
                    upazilla_id = int(self.data.get('upazilla'))
                    self.fields['union'].queryset = models.Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['union'].queryset = self.instance.upazilla.union_set.order_by('name')



class EducationInfoForm(forms.ModelForm):
    class Meta:
        model = models.EducationInfo
        fields = '__all__'
        widgets = {
            'name_of_exam': forms.TextInput(attrs={'class': 'form-control'}),
            'institute': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'board': forms.TextInput(attrs={'class': 'form-control'}),
            'passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TrainingInfoForm(forms.ModelForm):
    class Meta:
        model = models.TrainingInfo
        fields = '__all__'
        widgets = {
            'training_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
        }

class JobInfoForm(forms.ModelForm):
    class Meta:
        model = models.JobInfo
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'joning_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_designation': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'scale': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade_of_post': forms.TextInput(attrs={'class': 'form-control'}),
            'first_time_scale_due_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'second_time_scale_due_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'promotion_due_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'recreation_leave_due_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_retirement_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExperienceInfoForm(forms.ModelForm):
    class Meta:
        model = models.ExperienceInfo
        fields = '__all__'
        widgets = {
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddDesignationForm(forms.ModelForm):
    class Meta:
        model = models.Designation
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
