from django import forms
from academic.models import ClassRegistration, Session
from result.models import SubjectRegistration

class SearchEnrolledStudentForm(forms.Form):
    reg_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all())
    session = forms.ModelChoiceField(queryset=Session.objects.all())

class AttendanceForm(forms.Form):
    select_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all(), label="Class", required=False)
    session_year = forms.ModelChoiceField(queryset=Session.objects.all(), label="Session", required=False)
    student_roll = forms.IntegerField(label="Student Roll Number", required=False)
    subject = forms.ModelChoiceField(queryset=SubjectRegistration.objects.none(), label="Subject", required=False)

    def __init__(self, *args, **kwargs):
        class_id = kwargs.pop('class_id', None)
        session_id = kwargs.pop('session_id', None)
        super().__init__(*args, **kwargs)

        # Filter subjects by selected class
        if class_id:
            self.fields['subject'].queryset = SubjectRegistration.objects.filter(select_class__id=class_id)

        # Optionally, you can add filtering based on session if required.
        if session_id:
            # Add session filtering logic here if necessary
            pass
