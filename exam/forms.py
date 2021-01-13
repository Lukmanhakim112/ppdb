from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Div, HTML, Field
from crispy_forms.bootstrap import InlineField


from .models import Exam, Question, Answer


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
