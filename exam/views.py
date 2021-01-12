from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form

from . import forms, models


def retrive_answer(request, pk):
    answer = models.Answer.objects.filter(question=pk)
    return JsonResponse({'success': True, 'answer': answer}, status=200)


class ExamView(View):
    form_class = forms.ExamForm
    models = form_class.Meta.model
    template_name = 'exam/exam.html'

    def get(self, request, *args, **kwargs):
        data = self.models.objects.all()
        return render(request, self.template_name, {"form": self.form_class, "data": data})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return HttpResponse('success')

        return HttpResponse('fail', status=404)


class ExamViewDetail(ExamView):
    template_name = 'exam/exam_detail.html'

    def get(self, request, *args, **kwargs):
        data = self.models.objects.get(pk=self.kwargs['pk'])
        question = models.Question.objects.filter(exam=self.kwargs['pk'])
        question_count = question.count()
        return render(request, self.template_name, {"form": self.form_class, "data": data, "question": question, "question_count": question_count})


class AddQuestion(UserPassesTestMixin, View):
    template_name = 'exam/question_add.html'
    form_helper = forms.AnswerFormHelper

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        form_q = forms.QuestionForm
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
        form_q = forms.QuestionForm(request.POST, request.FILES or None)
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

class QuestionDeleteView(DeleteView):
    model = models.Question

    def get_success_url(self):
        return reverse_lazy('exam-detail', kwargs={'pk': self.kwargs['pk_exam']})


class QuestionUpdateView(UpdateView):
    pass

class QuestionView(View):
    form_class = forms.QuestionForm
    models = form_class.Meta.model
    template_name = 'exam/question.html'

    def get(self, request, *args, **kwargs):
        data = self.models.objects.filter(exam=self.kwargs['pk'])
        return render(request, self.template_name, {"form": self.form_class, "data": data})

class AnswerView(View):
    form_class = forms.AnswerForm
    models = form_class.Meta.model
    # template_name = 'exam/answer.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            data = list(self.models.objects.filter(question=self.kwargs['pk']).values('pk', 'answer_text', 'answer_image', 'is_right'))
        else:
            data = list(self.models.objects.filter(question=self.kwargs['pk']).values('pk', 'answer_text', 'answer_image'))

        return JsonResponse({'success': True, 'answer': data}, status=200)
