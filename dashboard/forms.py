from primaseru import models as prim_models
from primaseru import forms as prim_forms

from . import layouts

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
