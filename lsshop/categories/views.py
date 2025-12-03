from django.shortcuts import render

def categories(request):
    return render(request,  'categories/store.html', {'categories':categories})