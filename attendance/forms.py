from django import forms
from academic.models import ClassRegistration,Session


class SearchEnrolledStudentForm(forms.Form):
    reg_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all())
    session = forms.ModelChoiceField(queryset=Session.objects.all())