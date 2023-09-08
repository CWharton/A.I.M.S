from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def dashboard(request):
    return HttpResponseRedirect(reverse('assets:list'))
