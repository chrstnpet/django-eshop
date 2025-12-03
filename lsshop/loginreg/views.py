from django.shortcuts import render

def loginreg(request):
    return render(request, 'loginreg/loginreg.html', {'loginreg':loginreg})