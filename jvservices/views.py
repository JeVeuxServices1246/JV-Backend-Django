from django.http import HttpResponse

def index(request):
    return HttpResponse('<h2 style="text-align:center;margin-top:100px;">Welcome to JV services..</h2>')