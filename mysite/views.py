from django.shortcuts import render

def about(request):
    return render(request, 'mysite/about.html', {})