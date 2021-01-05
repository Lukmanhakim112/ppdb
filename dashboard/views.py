from django.shortcuts import render
from django.views.generic import UpdateView

from users.forms import CustomUserCreationForm
from primaseru import models as prim_models
from . import forms

class StudentDetailView(UpdateView):
    model = prim_models.StudentProfile
    form_class = forms.DashboardStudentProfileForm
    template_name = 'dashboard/student_detail.html'

def dashboard(request):
    siswa = prim_models.StudentProfile.objects.all()
    verified = prim_models.StudentProfile.objects.filter(verified=True).count()
    ctx = {
        'siswa': siswa,
        'siswa_verified': verified,
        'siswa_not_verified': siswa.count() - verified,
        'form_r': CustomUserCreationForm,
    }

    return render(request, 'dashboard/dashboard.html', context=ctx)
