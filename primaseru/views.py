from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from crispy_forms.utils import render_crispy_form

from .forms import StudentProfileForm, FatherStudentProfileForm, MotherStudentProfileForm, StudentGuardianProfileForm, MajorStudentForm, PhotoProfileForm, RaportForm
from .models import PhotoProfile


def home(request):
    return render(request, 'primaseru/home.html')

@login_required
def save_profile(request, data):
    if request.method == "POST":
        if data == "father":
            form = FatherStudentProfileForm(request.POST, instance=request.user.fatherstudentprofile)
        elif data == "mother":
            form = MotherStudentProfileForm(request.POST, instance=request.user.motherstudentprofile)
        elif data == "guardian":
            form = StudentGuardianProfileForm(request.POST, instance=request.user.studentguardianprofile)
        elif data == "profile":
            form = StudentProfileForm(request.POST, instance=request.user.studentprofile)
        elif data == "major":
            form = MajorStudentForm(request.POST, instance=request.user.majorstudent)
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
        form_ph = PhotoProfileForm(request.POST, request.FILES, instance=request.user.photoprofile)
        if form_ph.is_valid():
            form_ph.save()
            return redirect('profile')
    else:
        ctx = {'form_s': StudentProfileForm(instance=request.user.studentprofile),
               'form_f': FatherStudentProfileForm(instance=request.user.fatherstudentprofile),
               'form_m': MotherStudentProfileForm(instance=request.user.motherstudentprofile),
               'form_g': StudentGuardianProfileForm(instance=request.user.studentguardianprofile),
               'form_ma': MajorStudentForm(instance=request.user.majorstudent),
               'form_ph': PhotoProfileForm(instance=request.user.photoprofile),
               'form_r': RaportForm(),
               'profile': PhotoProfile.objects.get(student=request.user)
           }
        return render(request, 'primaseru/primaseru.html', context=ctx)

