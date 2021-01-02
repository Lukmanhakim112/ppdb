from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required

from crispy_forms.utils import render_crispy_form

from . import forms, models


class ParentView(View):
    form_class = forms.FatherStudentProfileForm
    models = models.FatherStudentProfile
    template_name = 'primaseru/parent_profile.html'
    name = "ayah"

    def get(self, request, *args, **kwargs):
        data = self.models.objects.get(child=request.user)
        form = self.form_class(instance=data)
        return render(request, self.template_name, {"form": form, "name": self.name})

    def post(self, request, *args, **kwargs):
        data = self.models.objects.get(child=request.user)
        form = self.form_class(request.POST, instance=data)

        ctx = {}
        ctx.update(csrf(request))
        form_s = render_crispy_form(form, context=ctx)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'form_s': form_s}, status=200)

        return JsonResponse({'success': False, 'form_s': form_s}, status=406)



def home(request):
    return render(request, 'primaseru/home.html')

@login_required
def save_profile(request, data):
    if request.method == "POST":
        if data == "profile":
            form = forms.StudentProfileForm(request.POST, instance=request.user.studentprofile)
        elif data == "major":
            form = forms.MajorStudentForm(request.POST, instance=request.user.majorstudent)
        else:
            return JsonResponse({'error': 'Not Find Any Person'}, status=404)

        ctx = {}
        ctx.update(csrf(request))
        form_s = render_crispy_form(form, context=ctx)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'form_s': form_s}, status=200)
        else:
            return JsonResponse({'success': False, 'form_s': form_s}, status=406)
    else:
        return redirect('profile')




@login_required
def studentProfile(request):
    if request.method == "POST":
        form_ph = forms.PhotoProfileForm(request.POST, request.FILES, instance=request.user.photoprofile)
        if form_ph.is_valid():
            form_ph.save()
            return redirect('profile')
    else:
        # TODO Refactoring This Fucking Shit!
        ctx = {'form_s': forms.StudentProfileForm(instance=request.user.studentprofile),
               'form_ma': forms.MajorStudentForm(instance=request.user.majorstudent),
               'form_ph': forms.PhotoProfileForm(instance=request.user.photoprofile),
               'form_r': forms.StudentFileForm(instance=request.user.studentfile),
               # Model,
               'photo': models.PhotoProfile.objects.get(student=request.user),
               'profile': models.StudentProfile.objects.get(student=request.user),
               'files': models.StudentFile.objects.get(student=request.user),
           }
        return render(request, 'primaseru/primaseru.html', context=ctx)

