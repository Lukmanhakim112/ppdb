from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.views import View
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from crispy_forms.utils import render_crispy_form
from xhtml2pdf import pisa

from . import forms, models
from .converter import link_callback_pdf
from dashboard.models import StudentStatus


def home(request):
    jadwal = models.RegisterSchedule.objects.all()

    return render(request, 'primaseru/timeline.html', {'jadwal': jadwal})

class ProfileView(LoginRequiredMixin, View):
    """
    Create base view for filling profile about student cadidate
    like: his/her father, mother, etc...
    father (Ayah) is the default here.
    """
    form_class = forms.FatherStudentProfileForm
    models = models.FatherStudentProfile
    template_name = 'primaseru/profile.html'
    name = "ayah"

    def get(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            raise PermissionDenied

        data = self.models.objects.get(student=request.user)
        form = self.form_class(instance=data)
        return render(request, self.template_name, {"form": form, "name": self.name, "data": data})

    def post(self, request, *args, **kwargs):
        data = self.models.objects.get(student=request.user)
        if data.verified:
            return JsonResponse({'success': False}, status=409)

        form = self.form_class(request.POST, request.FILES or None, instance=data)
        ctx = {}
        ctx.update(csrf(request))

        if form.is_valid():
            form.save()
            form = render_crispy_form(form, context=ctx)
            return JsonResponse({'success': True, 'form_s': form}, status=200)

        form = render_crispy_form(form, context=ctx)
        return JsonResponse({'success': False, 'form_s': form}, status=406)

class StudentProfileView(ProfileView):
    form_class = forms.StudentProfileForm
    models = models.StudentProfile
    name = "siswa"

class MoatherProfileView(ProfileView):
    form_class = forms.MotherStudentProfileForm
    models = models.MotherStudentProfile
    name = "ibu"

class GuardianProfileView(ProfileView):
    form_class = forms.StudentGuardianProfileForm
    models = models.StudentGuardianProfile
    name = "wali"

class MajorStudentView(ProfileView):
    form_class = forms.MajorStudentForm
    models = models.MajorStudent
    template_name = "primaseru/major.html"
    name = "jurusan"

class FilesStudentView(ProfileView):
    form_class = forms.StudentFileForm
    models = models.StudentFile
    template_name = "primaseru/student_files.html"
    name = "berkas"

def render_register_card_view(request):
    template_path = 'primaseru/register_card.html'
    profile = models.StudentProfile.objects.get(student=request.user)
    major = models.MajorStudent.objects.get(student=request.user)

    context = {
        'profile': profile,
        'major': major,
    }

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="Kartu Peserta_{request.user.full_name}.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback_pdf)

    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


@login_required
def studentProfile(request):
    if request.user.is_staff:
        return redirect('dashboard')

    if request.method == "POST":
        form_ph = forms.PhotoProfileForm(request.POST, request.FILES, instance=request.user.photoprofile)
        if form_ph.is_valid():
            form_ph.save()
            return redirect('profile')
    else:
        ctx = {
               'form_ph': forms.PhotoProfileForm(instance=request.user.photoprofile),
               'profile': models.PhotoProfile.objects.get(student=request.user),
               'status': StudentStatus.objects.get(student=request.user),
           }
        return render(request, 'primaseru/primaseru.html', context=ctx)
