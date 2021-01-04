from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.decorators import login_required

from crispy_forms.utils import render_crispy_form

from . import forms, models


def home(request):
    return render(request, 'primaseru/home.html')

class ProfileView(LoginRequiredMixin, View):
    form_class = forms.FatherStudentProfileForm
    models = models.FatherStudentProfile
    template_name = 'primaseru/profile.html'
    name = "ayah"

    def get(self, request, *args, **kwargs):
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


@login_required
def studentProfile(request):
    if request.method == "POST":
        form_ph = forms.PhotoProfileForm(request.POST, request.FILES, instance=request.user.photoprofile)
        if form_ph.is_valid():
            form_ph.save()
            return redirect('profile')
    else:
        ctx = {
               'form_ph': forms.PhotoProfileForm(instance=request.user.photoprofile),
               'profile': models.PhotoProfile.objects.get(student=request.user),
           }
        return render(request, 'primaseru/primaseru.html', context=ctx)
