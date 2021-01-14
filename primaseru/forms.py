from django import forms
import datetime

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
        self.form_tag = True
        self.helper.form_class = 'col-sm-12 form-horizontal'
        self.helper.label_class = 'col-sm-3 my-auto'
        self.helper.field_class = 'col-sm-9'
        self.helper.form_id = 'berkas-form'
        self.helper.layout = layouts.RAPORT_LAYOUT

    class Meta:
        model = StudentFile
        exclude = ['student', 'verified', 'msg', 'created_at', 'updated_at']


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
        self.form_tag = True
        self.helper.form_id = 'jurusan-form'
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
        self.form_tag = True
        self.helper.form_class = 'col-sm-12 parent-form'
        self.helper.form_id = 'ayah-form'
        self.helper.layout = layouts.PARENTS_LAYOUT

    class Meta:
        model =  FatherStudentProfile
        exclude = ['student', 'verified']

class MotherStudentProfileForm(forms.ModelForm):
    date_born = DATE_BORN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.form_tag = True
        self.helper.form_class = 'col-sm-12 parent-form'
        self.helper.form_id = 'ibu-form'
        self.helper.layout = layouts.PARENTS_LAYOUT

    class Meta:
        model =  MotherStudentProfile
        exclude = ['student', 'verified']

class StudentGuardianProfileForm(forms.ModelForm):
    date_born = DATE_BORN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.form_tag = True
        self.helper.form_class = 'col-sm-12 parent-form'
        self.helper.form_id = 'wali-form'
        self.helper.layout = layouts.PARENTS_LAYOUT

    class Meta:
        model =  StudentGuardianProfile
        exclude = ['student', 'verified']

class StudentProfileForm(forms.ModelForm):
    date_born = DATE_BORN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-md-12 '
        self.form_tag = True
        self.helper.form_id = 'siswa-form'
        self.helper.layout = layouts.STUDENT_LAYOUT

    class Meta:
        model =  StudentProfile
        exclude = ['student', 'verified']
