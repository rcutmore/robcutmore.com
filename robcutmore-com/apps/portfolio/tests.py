from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Project, ProjectTag
from .templatetags.portfolio_tags import get_project_list

def add_project_tag(title):
    """
    Adds and returns a new project tag with the given title.
    """
    tag = ProjectTag.objects.get_or_create(title=title)[0]
    return tag

def add_project(title, description, url='http://test.com', tags=None):
    """
    Adds and returns a new project with the given attributes.
    """
    project = Project.objects.get_or_create(
        title=title, description=description, url=url)[0]

    tags = tags if tags else []
    project_tags = [add_project_tag(tag) for tag in tags]
    project.tags.add(*project_tags)

    return project

class PortfolioTagsTests(TestCase):
    def test_get_project_list_with_no_projects(self):
        """
        get_project_list should return no projects when none exist.
        """
        result = get_project_list()

        self.assertQuerysetEqual(result['projects'].object_list, [])
        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_project_list_with_projects(self):
        """
        get_project_list should return existing projects.
        """
        first_project = add_project(title='1', description='1')
        second_project = add_project(title='2', description='2')

        result = get_project_list()

        projects = [first_project, second_project]
        result_projects = result['projects'].object_list

        for project in projects:
            self.assertTrue(project in result_projects)
        self.assertEqual(len(result_projects), len(projects))

        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_project_list_with_tag_filter(self):
        """
        get_project_list should return only projects with given tag.
        """
        tag = 'tag1'
        first_project = add_project(title='1', description='1', tags=[tag])
        second_project = add_project(title='2', description='2', tags=[tag])
        project_without_tag = add_project(title='3', description='3', tags=[])

        result = get_project_list(tag=tag)

        projects_with_tag = [first_project, second_project]
        result_projects = result['projects'].object_list

        for project_with_tag in projects_with_tag:
            self.assertTrue(project_with_tag in result_projects)
        self.assertFalse(project_without_tag in result_projects)
        self.assertEqual(len(result_projects), len(projects_with_tag))

        self.assertTrue(result['filtered'])
        self.assertEqual(result['tag'], tag)

    def test_get_project_list_with_page_filter(self):
        """
        get_project_list should return only projects for given page.
        """
        projects = [add_project(title=str(i), description=str(i)) for i in range(10)]
        first_page_projects = projects[:5]
        second_page_projects = projects[5:]

        # Test first page.
        result = get_project_list(page=1)
        first_page_result_projects = result['projects'].object_list

        for first_page_project in first_page_projects:
            self.assertTrue(first_page_project in first_page_result_projects)
        for second_page_project in second_page_projects:
            self.assertFalse(second_page_project in first_page_result_projects)

        # Test second page.
        result = get_project_list(page=2)
        second_page_result_projects = result['projects'].object_list

        for first_page_project in first_page_projects:
            self.assertFalse(first_page_project in second_page_result_projects)
        for second_page_project in second_page_projects:
            self.assertTrue(second_page_project in second_page_result_projects)

class ProjectListTests(TestCase):
    def test_project_list_with_no_projects(self):
        """
        project_list should display message when no projects exist.
        """
        response = self.client.get(reverse('portfolio:project_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no portfolio projects.')

    def test_project_list_with_projects(self):
        """
        project_list should display all projects.
        """
        first_project = add_project(title='1', description='1')
        second_project = add_project(title='2', description='2')

        response = self.client.get(reverse('portfolio:project_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_project.title)
        self.assertContains(response, first_project.description)
        self.assertContains(response, second_project.title)
        self.assertContains(response, second_project.description)

    def test_project_list_tags(self):
        """
        project_list should display project tags.
        """
        tags = ['tag1', 'tag2', 'tag3']
        project = add_project(title='1', description='1', tags=tags)

        response = self.client.get(reverse('portfolio:project_list'))

        self.assertEqual(response.status_code, 200)

        for tag in tags:
            self.assertContains(response, tag)

    def test_project_list_pagination(self):
        """
        project_list should display pagination buttons with more than 5 posts.
        """
        for i in range(15):
            add_project(title='{0}'.format(i), description='{0}'.format(i))

        url = reverse('portfolio:project_list')

        # Test first page.
        response = self.client.get(url)
        self.assertNotContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Test second page.
        response = self.client.get('{url}?page=2'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Test third page.
        response = self.client.get('{url}?page=3'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertNotContains(response, 'Next')