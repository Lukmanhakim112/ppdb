from django import forms
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Div, HTML, Field
from crispy_forms.bootstrap import InlineField

from .models import Exam, Question, Answer, Record, Score


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        exclude = ['student']


class ExamForm(forms.ModelForm):
    passcode = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(None,
                'exam_title',
                'passcode',
            ),
            HTML('<button role="submit" type="submit" class="btn btn-primary">Submit</button>'),
        )

    class Meta:
        model = Exam
        exclude = ['author']

class ExamEnrollForm(forms.Form):
    passcode = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Fieldset(None,
                    'passcode',
                    ),
            HTML('<button role="submit" type="submit" class="btn btn-primary">Go!</button>'),
        )

class CustomChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        if obj.answer_image:
            return mark_safe("<img src='%s' class='w-25 img-fluid' alt='image answer' />" % obj.answer_image.url)
        else:
            return obj.answer_text

class ExamTakeForm(forms.ModelForm):
    exam = forms.CharField(widget=forms.HiddenInput)
    question = forms.CharField(widget=forms.HiddenInput)
    answer = CustomChoiceField(queryset=Answer.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'answer-form'
        self.helper.form_method = 'post'

    class Meta:
        model = Record
        fields = ['exam', 'question', 'answer']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['exam']


class AnswerFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.disable_csrf = True
        self.use_custom_control = True
        FormHelper.form_tag = False
        self.template = 'bootstrap/table_inline_formset.html'


class AnswerForm(forms.ModelForm):


    class Meta:
        model = Answer
        exclude = ['question']

AnswerFormset = forms.modelformset_factory(Answer, form=AnswerForm, extra=4)
AnswerFormsetUpdate = forms.modelformset_factory(Answer, form=AnswerForm, can_delete=True)
