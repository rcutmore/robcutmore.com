from django.core.urlresolvers import reverse
from django.test import TestCase

from.models import Project

def add_project(title, description, url):
    project = Project.objects.get_or_create(
        title=title, description=description, url=url)[0]
    return project

class ProjectListTests(TestCase):
    def test_project_list_with_no_projects(self):
        """project_list should display message when no projects exist."""
        response = self.client.get(reverse('portfolio:project_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no portfolio projects.')
        self.assertQuerysetEqual(response.context['projects'], [])

    def test_project_list_with_projects(self):
        """project_list should display all projects."""
        first_project = add_project(
            'Project 1', 'Project 1 description', 'http://www.robcutmore.com')
        second_project = add_project(
            'Project 2', 'Project 2 description', 'http://www.robcutmore.com')

        response = self.client.get(reverse('portfolio:project_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_project.title)
        self.assertContains(response, first_project.description)
        self.assertContains(response, second_project.title)
        self.assertContains(response, second_project.description)

        project_count = len(response.context['projects'])
        self.assertEqual(project_count, 2)