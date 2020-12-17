from django.shortcuts import render
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form

from .forms import StudentProfileForm


def home(request):
    return render(request, 'primaseru/home.html')

def studentProfile(request):
    return render(request, 'primaseru/primaseru.html', context={'form_s': StudentProfileForm})
