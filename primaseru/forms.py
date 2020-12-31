from django import forms
import datetime
from django.urls import reverse

from crispy_forms.helper import FormHelper

from . import choices, layouts
from .models import StudentProfile, FatherStudentProfile, MotherStudentProfile, StudentGuardianProfile, MajorStudent, PhotoProfile, StudentFile


DATE_BORN = forms.DateField(label='Tanggal Lahir',initial=datetime.date.today, widget=forms.DateInput(format="%d/%m/%Y"),
                                help_text="Format: <em>DD/MM/YYYY</em>", input_formats=["%d/%m/%Y"])


class StudentFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-sm-12 form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-9'
        self.helper.form_id = 'raport-form'
        self.helper.layout = layouts.RAPORT_LAYOUT

    class Meta:
        model = StudentFile
        exclude = ['student', 'created_at', 'updated_at', 'verified', 'msg']


class PhotoProfileForm(forms.ModelForm):

    class Meta:
        model = PhotoProfile
        fields = ['image']

class MajorStudentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-sm-12 '
        self.helper.form_id = 'major-form'
        self.helper.layout = layouts.MAJOR_LAYOUT

    class Meta:
        model =  MajorStudent
        exclude = ['student', 'verified']

class FatherStudentProfileForm(forms.ModelForm):
    date_born = DATE_BORN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-sm-12 '
        self.helper.form_id = 'father-form'
        self.helper.layout = layouts.PARENTS_LAYOUT

    class Meta:
        model =  FatherStudentProfile
        exclude = ['child', 'verified']

class MotherStudentProfileForm(forms.ModelForm):
    date_born = DATE_BORN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-sm-12 '
        self.helper.form_id = 'mother-form'
        self.helper.layout = layouts.PARENTS_LAYOUT

    class Meta:
        model =  MotherStudentProfile
        exclude = ['child', 'verified']

class StudentGuardianProfileForm(forms.ModelForm):
    date_born = DATE_BORN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-sm-12 '
        self.helper.form_id = 'guardian-form'
        self.helper.layout = layouts.PARENTS_LAYOUT

    class Meta:
        model =  StudentGuardianProfile
        exclude = ['child', 'verified']

class StudentProfileForm(forms.ModelForm):
    date_born = DATE_BORN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-md-12 '
        self.helper.form_id = 'profile-form'
        self.helper.layout = layouts.STUDENT_LAYOUT

    class Meta:
        model =  StudentProfile
        exclude = ['student', 'verified']
