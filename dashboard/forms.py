from django import forms
import datetime

from primaseru import models as prim_models
from primaseru import forms as prim_forms

from . import layouts
from .models import StudentStatus

from crispy_forms.helper import FormHelper


class AddRegisterNumberForm(forms.ModelForm):

    class Meta:
        model = prim_models.StudentProfile
        fields = ['no_regis']


class StudentStatusForm(forms.ModelForm):
    CONFIRM = [
        (None, '=Pilih='),
        (True, 'Diterima'),
        (False, 'Tidak Diterima'),
    ]
    accepted = forms.ChoiceField(choices=CONFIRM, label='Status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.form_tag = True
        self.helper.form_class = 'col-sm-12 my-3 p-3 verified-form'
        self.helper.form_id = 'status-form'
        self.helper.layout = layouts.DASHBOARD_STATUS

    class Meta:
        model = StudentStatus
        exclude = ['student']

class RegisterScheduleForm(forms.ModelForm):

    start_date = forms.DateField(label='Tanggal Mulai',initial=datetime.date.today, widget=forms.DateInput(format="%d/%m/%Y"),
                                help_text="Format: <em>DD/MM/YYYY</em>", input_formats=["%d/%m/%Y"])

    end_date = forms.DateField(label='Tanggal Berakhir',initial=datetime.date.today, widget=forms.DateInput(format="%d/%m/%Y"),
                                help_text="Format: <em>DD/MM/YYYY</em>", input_formats=["%d/%m/%Y"])

    class Meta:
        model = prim_models.RegisterSchedule
        fields = '__all__'

class DashboardStudentProfileForm(prim_forms.StudentProfileForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = 'col-lg-12 col-md-12 my-3 p-3 verified-form'
        self.helper.form_id = 'siswa-form'
        self.helper.layout = layouts.DASHBOARD_STUDENT

    class Meta(prim_forms.StudentProfileForm.Meta):
        exclude = ['student']


class DashboardFilesForm(prim_forms.StudentFileForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = 'col-lg-12 col-md-12 my-3 p-3 verified-form'
        self.helper.form_id = 'berkas-form'
        self.helper.label_class = None
        self.helper.field_class = None
        self.helper.layout = layouts.DASHBOARD_FILES

    class Meta(prim_forms.StudentFileForm.Meta):
        exclude = ['student', 'created_at', 'updated_at']


class DashboardMajorForm(prim_forms.MajorStudentForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = 'col-lg-12 col-md-12 my-3 p-3 verified-form'
        self.helper.form_id = 'jurusan-form'
        self.helper.layout = layouts.DASHBOARD_MAJOR

    class Meta(prim_forms.MajorStudentForm.Meta):
        exclude = ['student']


class DashboardFatherForm(prim_forms.FatherStudentProfileForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = 'col-lg-12 col-md-12 my-3 p-3 verified-form'
        self.helper.form_id = 'ayah-form'
        self.helper.layout = layouts.DASHBOARD_PARENT

    class Meta(prim_forms.FatherStudentProfileForm.Meta):
        exclude = ['student']


class DashboardMotherForm(DashboardFatherForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'ibu-form'

    class Meta(DashboardFatherForm.Meta):
        model = prim_models.MotherStudentProfile

class DashboardGuardianForm(DashboardFatherForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'wali-form'

    class Meta(DashboardFatherForm.Meta):
        model = prim_models.StudentGuardianProfile


