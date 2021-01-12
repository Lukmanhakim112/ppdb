from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from users.forms import CustomUserCreationForm, CustomUserUpdateForm
from primaseru import models as prim_models
from exam.models import Exam, Question
from . import forms

class UpdateUser(UserPassesTestMixin, UpdateView):
    model = CustomUserUpdateForm.Meta.model
    form_class = CustomUserUpdateForm
    template_name = 'dashboard/student_change.html'

    def get_success_url(self):
        return reverse_lazy('detail-student', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user.is_staff

class ProfileDetailView(UserPassesTestMixin, UpdateView):
    form_class = forms.DashboardStudentProfileForm
    template_name = 'dashboard/student_detail.html'

    def get_object(self):
        return self.form_class.Meta.model.objects.get(student=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calon_pk'] = self.kwargs['pk']
        context['name'] = self.object.student.full_name
        return context

    def get_success_url(self):
        return reverse_lazy('detail-student', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user.is_staff


class FatherProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardFatherForm

class MotherProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardMotherForm

class GuardianProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardGuardianForm

class MajorProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardMajorForm

class FilesProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardFilesForm

@login_required
def exam_list(request):

    if not request.user.is_staff:
        return redirect('profile')

    exam = Exam.objects.all()

    return render(request, 'dashboard/exam.html', context={'exam': exam})

@login_required
def dashboard(request):

    if not request.user.is_staff:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    siswa = prim_models.StudentProfile.objects.all()
    verified = prim_models.StudentProfile.objects.filter(verified=True).count()
    ctx = {
        'siswa': siswa,
        'siswa_verified': verified,
        'siswa_not_verified': siswa.count() - verified,
        'form_r': CustomUserCreationForm,
    }

    return render(request, 'dashboard/dashboard.html', context=ctx)
