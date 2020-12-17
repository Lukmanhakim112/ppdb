from django import forms
import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Row, Div, HTML, Field
from crispy_forms.bootstrap import TabHolder, Tab

from . import choices
from .models import StudentProfile, FatherStudentProfile


class StudentProfileForm(forms.ModelForm):
    date_born = forms.DateField(label='Tanggal Lahir',initial=datetime.date.today, widget=forms.DateInput(format="%d/%m/%Y"),
                                help_text="Format: DD/MM/YYYY")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-md-12 '
        self.helper.form_id = 'profile-form'
        self.helper.use_custom_control = True
        self.helper.layout = Layout(
            Fieldset(None, # Set first arg to none because of leaking or it does not render
                TabHolder(
                    Tab('Data Diri',
                        Row(
                            Div(Field("sex", css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                            Div(Field('religion', css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("handpone", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('email', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("city_born", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('date_born', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("social_media", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('school_origin', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("resident", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('transport', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("npsn_school_origin", css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                    ),
                    Tab('Alamat',
                        Row(
                            Div(Field("nik", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('nisn', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("address_kk", css_class='form-control-sm kk-autosize'), css_class="col-sm-6"),
                            Div(Field('no_kk', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("province", css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                            Div(Field('city', css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("kecamatan", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('kelurahan', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("rt_rw", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('real_address', css_class='form-control-sm', css_id="real-address"), css_class="col-sm-6"),
                        ),
                    ),
                    Tab('Cat. Kesehatan',
                        Row(
                            Div(Field("blood_type", css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                            Div(Field('in_medicine', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("private_doctor", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('phone_doctor', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field('medic_record', css_class='form-control-sm autoresize'), css_class="col-sm-12"),
                        ),
                    ),
                ),
                HTML('<hr />'),
                HTML('\
                    <button type="submit" role="submit" class="btn btn-outline-primary btn-block"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-check2-all" viewBox="0 0 16 16"> \
  <path fill-rule="evenodd" d="M12.354 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/> \
  <path d="M6.25 8.043l-.896-.897a.5.5 0 1 0-.708.708l.897.896.707-.707zm1 2.414l.896.897a.5.5 0 0 0 .708 0l7-7a.5.5 0 0 0-.708-.708L8.5 10.293l-.543-.543-.707.707z"/> \
</svg> Save</button> \
                ')
            ),
        )

    class Meta:
        model =  StudentProfile
        exclude = ['student']
