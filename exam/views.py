from itertools import islice

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView, ListView
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form
from users.views import UserIsStaffMixin, PassEnrollMixin

from . import forms, models

class ExamView(LoginRequiredMixin, View):
    form_class = forms.ExamForm
    models = form_class.Meta.model
    template_name = 'exam/exam.html'

    def get(self, request, *args, **kwargs):

        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            raise PermissionDenied

        data = self.models.objects.all()
        return render(request, self.template_name, {"data": data})


class ExamViewDetail(UserIsStaffMixin, ExamView):
    template_name = 'exam/exam_detail.html'

    def get(self, request, *args, **kwargs):
        data = self.models.objects.get(pk=self.kwargs['pk'])
        question = models.Question.objects.filter(exam=self.kwargs['pk'])
        question_count = question.count()
        return render(request, self.template_name, {"form": self.form_class, "data": data, "question": question, "question_count": question_count})


class ExamUpdateView(UserIsStaffMixin, UpdateView):
    model = models.Exam
    form_class = forms.ExamForm
    template_name = 'exam/exam_update.html'
    success_url = '/dashboard/exam/'

class ExamDeleteView(UserIsStaffMixin, DeleteView):
    model = models.Exam
    success_url = '/dashboard/exam/'


class ExamEnrollView(LoginRequiredMixin, View):
    form_class = forms.ExamEnrollForm
    model = models.Exam

    def get(self, request, *args, **kwargs):
        form = self.form_class
        exam = self.model.objects.get(pk=self.kwargs['pk'])

        return render(request, 'exam/exam_enroll.html', {'form': form, 'exam': exam})

    def post(self, request, *args, **kwargs):
        form = self.form_class
        exam = self.model.objects.get(pk=self.kwargs['pk'])
        message = "Passcode Tidak Valid!"

        if exam.passcode == request.POST['passcode']:
            request.session[f'exam_{exam.pk}_enroll'] = True
            request.session[f'exam_{exam.pk}_timer'] = int(exam.duration) * 60
            return redirect('taken-question', pk_exam=exam.pk)

        return render(request, 'exam/exam_enroll.html', {'form': form, 'message': message, 'exam': exam})

class ExamTimerView(PassEnrollMixin, View):
    form_class = forms.TimerForm

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk_exam']
        time = self.request.session[f'exam_{pk}_timer']
        return JsonResponse({'time': time})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        exam = self.kwargs['pk_exam']

        if form.is_valid():
            request.session[f'exam_{exam}_timer'] = form.cleaned_data['timerExam']
            return JsonResponse({'success': True})

        return JsonResponse({'success': False}, status=406)

class ExamTimesUpView(PassEnrollMixin, View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk_exam']

        request.session[f'exam_{pk}_times_up'] = True

        return JsonResponse({'success': True})

class TakeExamView(PassEnrollMixin, ListView):
    model = models.Question
    paginate_by = 1
    # context_object_name = 'question_list'

    def get_queryset(self):
        query = get_object_or_404(models.Exam, pk=self.kwargs['pk_exam'])
        return self.model.objects.filter(exam=query).order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_exam = self.kwargs['pk_exam']
        context['pk_exam'] = pk_exam
        context['timerForm'] = forms.TimerForm
        return context

class AnswerView(LoginRequiredMixin, View):
    models = models.Answer
    # template_name = 'exam/answer.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            data = list(self.models.objects.filter(question=self.kwargs['pk']).values('answer_text', 'answer_image', 'is_right'))
        else:
            data = list(self.models.objects.filter(question=self.kwargs['pk']).values('answer_text', 'answer_image'))

        return JsonResponse({'success': True, 'answer': data}, status=200)

class RetriveAnswer(AnswerView):
    form_class = forms.ExamTakeForm
    template_name = 'exam/exam_form.html'

    def get(self, request, *args, **kwargs):
        data = {
            'exam' : self.kwargs['pk_exam'],
            'question' : self.kwargs['pk'],
        }
        formState = request.session.get(f'{data["exam"]}-{data["question"]}-answer')
        form = self.form_class(initial=formState or data)
        form.fields['answer'].queryset = self.models.objects.filter(question=self.kwargs['pk'])

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST, instance=request.user)
        request.session[f'{kwargs["pk_exam"]}-{kwargs["pk"]}-answer'] = request.POST

        return JsonResponse({'success': True}, status=200)

class SubmitAnswer(RetriveAnswer):
    model = models.Exam
    template_name = 'exam/answer_confirmation.html'

    def get(self, request, *args, **kwargs):
        exam = self.model.objects.get(pk=self.kwargs['pk_exam'])
        check_score = models.Score.objects.filter(student=request.user, exam=exam).exists()

        if check_score:
            raise PermissionDenied

        return render(request, self.template_name, {'exam': exam})

    def post(self, request, *args, **kwargs):

        exam = self.model.objects.get(pk=self.kwargs['pk_exam'])
        question = models.Question.objects.filter(exam=exam)
        score = 0

        # REVIEW Need refactor? I think so...
        total_question = []
        for q in question:

            try:
                data = request.session.get(f'{exam.pk}-{q.pk}-answer') # Retrive data from the session
                answer = models.Answer.objects.get(pk=int(data['answer'])) # Retrive the answer
                record = models.Record(exam=exam, question=q, answer=answer, student=request.user) # Create the object
                total_question.append(record) # Add it to the list, and then bulk insert it

                if record.answer.is_right:
                    score += 1

            except (KeyError, ValueError, models.Answer.DoesNotExist, TypeError):
                pass

        # Add the score to DB
        persentage = score / len(question) * 100
        models.Score.objects.create(student=request.user, exam=exam, score=score, persentage=persentage)

        # Bulk create the record (history)
        models.Record.objects.bulk_create(total_question)
        return render(request, 'exam/exam_finish.html')



class AddQuestion(UserIsStaffMixin, View):
    form_class = forms.QuestionForm
    template_name = 'exam/question_add.html'
    form_helper = forms.AnswerFormHelper

    def get(self, request, *args, **kwargs):
        form_q = self.form_class
        form_a = forms.AnswerFormset(queryset=models.Answer.objects.none())
        context = {
            'form_a': form_a,
            'form_q': form_q,
            'helper': self.form_helper(),
            'exam': models.Exam.objects.get(pk=self.kwargs['pk']),
            'question_count': models.Question.objects.filter(exam=self.kwargs['pk']).count(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form_q = self.form_class(request.POST, request.FILES or None)
        form_a = forms.AnswerFormset(request.POST, request.FILES or None)

        if form_q.is_valid() and form_a.is_valid():
            form_q.instance.exam = models.Exam.objects.get(pk=self.kwargs['pk'])
            question = form_q.save()

            answer_instance = form_a.save(commit=False)
            for a in answer_instance:
                a.question = question
                a.save()

            question_count = models.Question.objects.filter(exam=self.kwargs['pk']).count(),
            return JsonResponse({'success': True, 'question_count': question_count}, status=200)

        ctx = {}
        ctx.update(csrf(request))
        form_q = render_crispy_form(form_q, context=ctx)
        form_a = render_crispy_form(form_a)

        return JsonResponse({'success': False, 'form_q': form_q, 'form_a': form_a}, status=409)

class QuestionDeleteView(UserIsStaffMixin, DeleteView):
    model = models.Question

    def get_success_url(self):
        return reverse_lazy('exam-detail', kwargs={'pk': self.kwargs['pk_exam']})


class QuestionUpdateView(AddQuestion):
    model = models.Question
    template_name = 'exam/question_update.html'

    def get(self, request, *args, **kwargs):
        question = self.model.objects.get(pk=self.kwargs['pk'])
        form_q = self.form_class(instance=question)
        form_a = forms.AnswerFormsetUpdate(queryset=models.Answer.objects.filter(question=question))
        context = {
            'form_q': form_q,
            'form_a': form_a,
            'helper': self.form_helper(),
            'exam': models.Exam.objects.get(pk=self.kwargs['pk_exam']),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        question = self.model.objects.get(pk=self.kwargs['pk'])
        form_q = self.form_class(request.POST, request.FILES or None, instance=question)
        form_a = forms.AnswerFormsetUpdate(request.POST, request.FILES or None)

        if form_q.is_valid() and form_a.is_valid():
            question = form_q.save()

            answer_instance = form_a.save(commit=False)

            for deleted_obj in form_a.deleted_objects:
                deleted_obj.delete() # Deleting Answer

            for obj in answer_instance:
                obj.question = question
                obj.save()

            return redirect('exam-detail', pk=question.exam.pk)

        return HttpResponse('fail', status=400)

