from django.shortcuts import render

from .models import Project

def project_list(request):
    projects = Project.objects.all()
    context_dict = {'projects': projects, 'active_page': 'portfolio'}

    return render(request, 'portfolio/project_list.html', context_dict)