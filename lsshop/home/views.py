from django.shortcuts import render

def home(request):
    context = {
        'show_secondary_header': True,
        'home' : 'home'
    }
    return render(request, 'home/home.html', context)