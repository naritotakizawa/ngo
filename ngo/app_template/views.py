from ngo.template import render


def home(request):
    return render(request, '{app_name}/home.html')
