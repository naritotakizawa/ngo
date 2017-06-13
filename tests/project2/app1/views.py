from ngo.template import render

def home(request):
    return render(request, 'app1/home.html')
