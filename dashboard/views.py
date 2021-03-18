import datetime

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import UpdateView, View, ListView, DeleteView, CreateView
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.views import UserIsStaffMixin
from users.forms import CustomUserCreationForm, CustomUserUpdateForm
from users.models import CustomUser

from primaseru import models as prim_models

from .models import StudentStatus
from .forms import AddRegisterNumberForm

from exam.forms import ExamForm, ScoreForm
from exam.models import Exam, Score

import xlwt

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

    if not request.user.is_staff:
        return redirect('profile')

    form = CustomUserCreationForm()
    form_a = AddRegisterNumberForm()
    form_error = 'false'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        form_a = AddRegisterNumberForm(request.POST)
        if form.is_valid() and form_a.is_valid():
            form = form.save()
            form_a.instance.student = form
            form_a.save()
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
        'form_a': form_a,
        'form_error': form_error,
    }

    return render(request, 'dashboard/dashboard.html', context=ctx)

@login_required
def export_excel(request):
    if not request.user.is_staff:
        return redirect('profile')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Pendaftar_Primaseru.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Pendaftar Primaseru')

    student_names = CustomUser.objects.filter(is_staff=False).values_list('full_name', flat=True)
    profile_fields = prim_models.StudentProfile._meta.get_fields()[3:]

    font_style = xlwt.XFStyle()
    ws.write(0, 0, 'Nama Lengkap', font_style)
    row_num = 0

    header = [n.verbose_name for n in profile_fields]
    for col_num in range(len(header)):
        ws.write(row_num, col_num+1, header[col_num], font_style)

    columns = [n.name for n in profile_fields]
    rows = prim_models.StudentProfile.objects.all().values_list(*columns)

    for i in range(len(student_names)):
        ws.write(i+1, 0, student_names[i], font_style)

    for row in rows:
        row_num += 1

        col_num = 1
        for data in row:
            try:
                data = data.strftime('%d-%m-%Y')
                data = data.get_sex_display()
            except AttributeError:
                pass

            ws.write(row_num, col_num, data, font_style)
            col_num += 1

    wb.save(response)
    return response
