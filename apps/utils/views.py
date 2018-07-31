from django.http import HttpResponseRedirect
from .services import GoogleFlow

def auth(request):
    flow = GoogleFlow()
    auth_url = flow.autorization_url()
    return HttpResponseRedirect(auth_url)