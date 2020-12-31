from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required

from crispy_forms.utils import render_crispy_form

from . import forms, models

def home(request):
    return render(request, 'primaseru/home.html')

@login_required
def save_profile(request, data):
    if request.method == "POST":
        if data == "father":
            form = forms.FatherStudentProfileForm(request.POST, instance=request.user.fatherstudentprofile)
        elif data == "mother":
            form = forms.MotherStudentProfileForm(request.POST, instance=request.user.motherstudentprofile)
        elif data == "guardian":
            form = forms.StudentGuardianProfileForm(request.POST, instance=request.user.studentguardianprofile)
        elif data == "profile":
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
               'form_f': forms.FatherStudentProfileForm(instance=request.user.fatherstudentprofile),
               'form_m': forms.MotherStudentProfileForm(instance=request.user.motherstudentprofile),
               'form_g': forms.StudentGuardianProfileForm(instance=request.user.studentguardianprofile),
               'form_ma': forms.MajorStudentForm(instance=request.user.majorstudent),
               'form_ph': forms.PhotoProfileForm(instance=request.user.photoprofile),
               'form_r': forms.StudentFileForm(instance=request.user.studentfile),
               # Model,
               'photo': models.PhotoProfile.objects.get(student=request.user),
               'profile': models.StudentProfile.objects.get(student=request.user),
               'father': models.FatherStudentProfile.objects.get(child=request.user),
               'mother': models.MotherStudentProfile.objects.get(child=request.user),
               'guardian': models.StudentGuardianProfile.objects.get(child=request.user),
               'files': models.StudentFile.objects.get(student=request.user),
           }
        return render(request, 'primaseru/primaseru.html', context=ctx)

