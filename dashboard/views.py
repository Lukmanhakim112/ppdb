from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from users.views import UserIsStaffMixin
from users.forms import CustomUserCreationForm, CustomUserUpdateForm

from primaseru import models as prim_models

from exam.forms import ExamForm
from exam.models import Exam

from . import forms


class ExamCreateView(UserIsStaffMixin, View):
    model = Exam
    form_class = ExamForm
    template_name = 'dashboard/exam.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        exam = self.model.objects.all()

        return render(request, 'dashboard/exam.html', {'form': form, 'exam': exam})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.instance.author = request.user
            exam = form.save()

            return redirect('exam-detail', pk=exam.pk)

        return redirect('dashboard-exam')


class UpdateUser(UserIsStaffMixin, UpdateView):
    model = CustomUserUpdateForm.Meta.model
    form_class = CustomUserUpdateForm
    template_name = 'dashboard/student_change.html'

    def get_success_url(self):
        return reverse_lazy('detail-student', kwargs={'pk': self.kwargs['pk']})

class ProfileDetailView(UserIsStaffMixin, UpdateView):
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

    paginator = Paginator(siswa, 10)
    page_number = request.GET.get('page')
    page_siswa = paginator.get_page(page_number)
    ctx = {
        'siswa': page_siswa,
        'jumlah_siswa': siswa.count(),
        'siswa_verified': verified,
        'siswa_not_verified': siswa.count() - verified,
        'form_r': CustomUserCreationForm,
    }

    return render(request, 'dashboard/dashboard.html', context=ctx)
