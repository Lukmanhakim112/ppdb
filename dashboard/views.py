from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View, ListView, DeleteView, CreateView
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.views import UserIsStaffMixin
from users.forms import CustomUserCreationForm, CustomUserUpdateForm
from users.models import CustomUser

from primaseru import models as prim_models
from .models import StudentStatus

from exam.forms import ExamForm, ScoreForm
from exam.models import Exam, Score

from . import forms


class RegisterSchedule(UserIsStaffMixin, ListView):
    template_name = "dashboard/registerschedule_list.html"
    model = prim_models.RegisterSchedule

class RegisterScheduleCreateView(UserIsStaffMixin, CreateView):
    model = prim_models.RegisterSchedule
    form_class = forms.RegisterScheduleForm
    template_name = "dashboard/registerschedule_form.html"
    success_url = '/dashboard/jadwal/pendaftaran/'

class RegisterSchduleDeleteView(UserIsStaffMixin, DeleteView):
    model = prim_models.RegisterSchedule
    success_url = '/dashboard/jadwal/pendaftaran/'

class RegisterSchduleUpdateView(UserIsStaffMixin, UpdateView):
    model = prim_models.RegisterSchedule
    form_class = forms.RegisterScheduleForm
    template_name = "dashboard/registerschedule_form.html"
    success_url = '/dashboard/jadwal/pendaftaran/'

class ProfileDeleteView(UserIsStaffMixin, DeleteView):
    model = prim_models.CustomUser
    success_url = '/dashboard/'


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
        return reverse('detail-student', kwargs={'pk': self.kwargs['pk']})

class ProfileDetailView(UserIsStaffMixin, UpdateView):
    form_class = forms.DashboardStudentProfileForm
    template_name = 'dashboard/student_detail.html'
    url_name = 'detail-student'

    def get_object(self):
        return self.form_class.Meta.model.objects.get(student=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calon_pk'] = self.kwargs['pk']
        context['name'] = self.object.student.full_name
        context['photo'] = prim_models.PhotoProfile.objects.get(student=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse(self.url_name, kwargs={'pk': self.kwargs['pk']})

class FatherProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardFatherForm
    url_name = 'detail-student-father'

class MotherProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardMotherForm
    url_name = 'detail-student-mother'

class GuardianProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardGuardianForm
    url_name = 'detail-student-guardian'

class MajorProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardMajorForm
    url_name = 'detail-student-major'

class FilesProfileDetailView(ProfileDetailView):
    form_class = forms.DashboardFilesForm
    url_name = 'detail-student-files'

class StatusStudentDetailView(ProfileDetailView):
    form_class = forms.StudentStatusForm
    url_name = 'detail-student-status'

class ScoreListView(UserIsStaffMixin, ListView):
    model = Score
    context_object_name = 'score_list'
    template_name = 'dashboard/score_list.html'

    def get_queryset(self):
        student = CustomUser.objects.get(pk=self.kwargs['pk'])
        return self.model.objects.filter(student=student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calon_pk'] = self.kwargs['pk']
        context['photo'] = prim_models.PhotoProfile.objects.get(student=self.kwargs['pk'])
        return context

class ScoreDeleteView(UserIsStaffMixin, DeleteView):
    model = Score

    def get_success_url(self):
        return reverse('detail-student-score', kwargs={'pk': self.kwargs['pk_user']})

@login_required
def dashboard(request):
    form = CustomUserCreationForm()
    form_error = 'false'
    if not request.user.is_staff:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            form_error = 'true'

    siswa = prim_models.StudentProfile.objects.all().order_by('-student')
    siswa_accepted = StudentStatus.objects.filter(accepted=True).count()
    verified = siswa.filter(verified=True).count()

    paginator = Paginator(siswa, 10)
    page_number = request.GET.get('page')
    page_siswa = paginator.get_page(page_number)

    ctx = {
        'siswa': page_siswa,
        'jumlah_siswa': siswa.count(),
        'siswa_verified': verified,
        'siswa_not_verified': siswa.count() - verified,
        'siswa_accepted': siswa_accepted,
        'form_r': form,
        'form_error': form_error,
    }

    return render(request, 'dashboard/dashboard.html', context=ctx)
