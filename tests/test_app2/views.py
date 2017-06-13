from ngo.template import render

def home(request):
    return render(request, 'test_app2/home.html')
