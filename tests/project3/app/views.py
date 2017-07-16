from ngo.template import render


def home(request):
    context = {}
    if request.method == 'POST':
        file1 = request.FILES.get('files')
        if file1:
            context['file1_name'] = file1.file_name
            file1.save()

        file2 = request.FILES.getlist('files2')
        names = []
        if file2:
            for f in file2:
                f.save()
                names.append(f.file_name)
            context['file2_name'] = names

        context['text'] = request.POST.get('text')
        context['text2'] = request.POST.get('text2')
        context['select'] = request.POST.getlist('select')

    elif request.method == 'GET':
        context['text'] = request.GET.get('text')
        context['text2'] = request.GET.get('text2')
        context['select'] = request.GET.getlist('select')
    return render(request, 'app/home.html', context)
