from ngo.template import render

def home(request):
    return render(request, 'app2/home.html')

def hello(request, name):
    context = {
        'name': name
    }
    return render(request, 'app2/hello.html', context)