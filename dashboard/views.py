from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from users.forms import CustomUserCreationForm
from primaseru import models as prim_models
from . import forms


class ProfileDetailView(UserPassesTestMixin, UpdateView):
    model = prim_models.StudentProfile
    form_class = forms.DashboardStudentProfileForm
    template_name = 'dashboard/student_detail.html'

    def get_object(self):
        return self.model.objects.get(student=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calon_pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('detail-student', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.is_staff


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
