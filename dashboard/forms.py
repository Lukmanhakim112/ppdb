from primaseru import models as prim_models
from primaseru import forms as prim_forms

class DashboardStudentProfileForm(prim_forms.StudentProfileForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta(prim_forms.StudentProfileForm.Meta):
        exclude = ['student']
