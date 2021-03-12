from crispy_forms.layout import Layout, Fieldset, Row, Div, HTML, Field
from crispy_forms.bootstrap import TabHolder, Tab, Accordion, AccordionGroup

STUDENT_BASE_LAYOUT = Layout(
            Fieldset(None,
                Accordion(
                    AccordionGroup("Data Diri",
                        Row(
                            Div(Field("sex", css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                            Div(Field('religion', css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("handpone", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field("social_media", css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("city_born", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('date_born', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field('school_origin', css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field("npsn_school_origin", css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field('nisn', css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field("no_regis", css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("nik", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('no_kk', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field('achievement', css_class='form-control-sm'), css_class="col-sm-12"),
                        ),
                    ),
                    AccordionGroup("Alamat",
                        Row(
                            Div(Field("resident", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('transport', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field('city', css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field("kecamatan", css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("dusun", css_class='form-control-sm'), css_class="col-sm-4"),
                            Div(Field('kelurahan', css_class='form-control-sm'), css_class="col-sm-4"),
                            Div(Field("rt_rw", css_class='form-control-sm'), css_class="col-sm-4"),
                        ),
                        Row(
                            Div(Field("address_kk", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('real_address', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                    ),
                    AccordionGroup("Catatan Kesehatan",
                        Row(
                            Div(Field("blood_type", css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                            Div(Field('in_medicine', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field("private_doctor", css_class='form-control-sm'), css_class="col-sm-6"),
                            Div(Field('phone_doctor', css_class='form-control-sm'), css_class="col-sm-6"),
                        ),
                        Row(
                            Div(Field('medic_record', css_class='form-control-sm  auto-size'), css_class="col-sm-12"),
                        ),
                    )
                ),
            ),
        )


PARENT_BASE_LAYOUT = Layout(
            Fieldset(None,
                Row(
                    Div(Field('full_name', css_class='form-control-sm'), css_class="col-sm-12"),
                ),
                Row(
                    Div(Field('city_born', css_class='form-control-sm'), css_class="col-sm-6"),
                    Div(Field('date_born', css_class='form-control-sm'), css_class="col-sm-6"),
                ),
                Row(
                    Div(Field('nik', css_class='form-control-sm'), css_class="col-sm-6"),
                    Div(Field('education', css_class='custom-select custom-select-sm'), css_class="col-sm-6"),
                ),
                Row(
                    Div(Field('job', css_class='form-control-sm'), css_class="col-sm-6"),
                    Div(Field('salary', css_class='form-control-sm'), css_class="col-sm-6"),
                ),
                Row(
                    Div(Field('email', css_class='form-control-sm'), css_class="col-sm-6"),
                    Div(Field('phone', css_class='form-control-sm'), css_class="col-sm-6"),
                ),
            )
        )

MAJOR_BASE_LAYOUT = Layout(
    Fieldset(None,
             Field('first_major', css_class="custom-select custom-select-sm"),
             Field('second_major', css_class="custom-select custom-select-sm"),
             Field('info', css_class="form-control-sm"),
    )
)


FILE_BASE_LAYOUT = Layout(
            Fieldset(None,
                Row(
                    Div('ra_sem_1', css_class="col-sm-12"),
                ),
                Row(
                    Div('ra_sem_2', css_class="col-sm-12"),
                ),
                Row(
                    Div('ra_sem_3', css_class="col-sm-12"),
                ),
                Row(
                    Div('ra_sem_4', css_class="col-sm-12"),
                ),
                Row(
                    Div('ra_sem_5', css_class="col-sm-12"),
                ),
                Row(
                    Div('color_blind_cert', css_class="col-sm-12"),
                ),
                Row(
                    Div('healty_cert', css_class="col-sm-12"),
                ),
            )
        )
