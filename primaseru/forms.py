from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Row, Div, HTML, Field

from . import choices
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model =  StudentProfile
        exclude = ['student']
