"""
Contains tests for portfolio app.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Project, ProjectTag
from .templatetags.portfolio_tags import get_project_list


def add_project_tag(title):
    """Add new project tag with given title.

    :param title: Title of tag.
    :returns: :class:`ProjectTag` object.
    """
    return ProjectTag.objects.get_or_create(title=title)[0]


def add_project(title, description, url='http://test.com', tags=None):
    """Add new project with given attributes.

    :param title: Title of project.
    :param description: Description of project.
    :param url: URL for project.
    :param tags: Tags to assign project.
    :returns: :class:`Project` object.
    """
    # Create project.
    project = Project.objects.get_or_create(
        title=title, description=description, url=url)[0]

    # Add tags to project.
    tags = tags if tags else []
    project_tags = [add_project_tag(tag) for tag in tags]
    project.tags.add(*project_tags)
    return project


class PortfolioTemplateTagsTests(TestCase):
    """Tests custom template tags for portfolio app."""

    def test_get_project_list_with_no_projects(self):
        """get_project_list should return no projects when none exist."""
        result = get_project_list()
        self.assertQuerysetEqual(result['projects'].object_list, [])
        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_project_list_with_projects(self):
        """get_project_list should return existing projects."""
        # Add two test projects.
        projects = [
            add_project(title='1', description='1'),
            add_project(title='2', description='2'),
        ]

        result = get_project_list()
        result_projects = result['projects'].object_list

        # Make sure two test projects are retrieved.
        for project in projects:
            self.assertTrue(project in result_projects)
        self.assertEqual(len(result_projects), len(projects))
        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_project_list_with_tag_filter(self):
        """get_project_list should return only projects with given tag."""
        # Add test projects.
        tag = 'tag1'
        projects_with_tag = [
            add_project(title='1', description='1', tags=[tag]),
            add_project(title='2', description='2', tags=[tag]),
        ]
        project_without_tag = add_project(title='3', description='3', tags=[])

        result = get_project_list(tag=tag)
        result_projects = result['projects'].object_list

        # Make sure only projects with tag are retrieved.
        for project_with_tag in projects_with_tag:
            self.assertTrue(project_with_tag in result_projects)
        self.assertFalse(project_without_tag in result_projects)
        self.assertEqual(len(result_projects), len(projects_with_tag))
        self.assertTrue(result['filtered'])
        self.assertEqual(result['tag'], tag)

    def test_get_project_list_with_page_filter(self):
        """get_project_list should return only projects for given page."""
        # Add test projects.
        projects = [
            add_project(title=str(i), description=str(i)) for i in range(10)
        ]

        first_page_projects = projects[:5]
        second_page_projects = projects[5:]

        # Check first page results.
        result = get_project_list(page=1)
        first_page_results = result['projects'].object_list
        for first_page_project in first_page_projects:
            self.assertTrue(first_page_project in first_page_results)
        self.assertFalse(
            any(project in first_page_results for project in second_page_projects))

        # Check second page results.
        result = get_project_list(page=2)
        second_page_results = result['projects'].object_list
        self.assertFalse(
            any(project in second_page_results for project in first_page_projects))
        for second_page_project in second_page_projects:
            self.assertTrue(second_page_project in second_page_results)


class ProjectListTests(TestCase):
    """Tests project list page of portfolio app."""

    def test_project_list_with_no_projects(self):
        """project_list should display message when no projects exist."""
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no portfolio projects.')

    def test_project_list_with_projects(self):
        """project_list should display all projects."""
        # Add test projects.
        first_project = add_project(title='Title 1', description='Description 1')
        second_project = add_project(title='Title 2', description='Description 2')

        # Check that project list contains test projects.
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_project.title)
        self.assertContains(response, first_project.description)
        self.assertContains(response, second_project.title)
        self.assertContains(response, second_project.description)

    def test_project_list_tags(self):
        """project_list should display project tags."""
        # Add test project with tags.
        tags = ['tag1', 'tag2', 'tag3']
        add_project(title='1', description='1', tags=tags)

        # Check that project list contains each tag.
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertEqual(response.status_code, 200)
        for tag in tags:
            self.assertContains(response, tag)

    def test_project_list_pagination(self):
        """project_list should display pagination buttons for many projects."""
        # Add enough projects so that pagination is required.
        # project_list should show 5 projects per page, so 15
        # projects will be split up over 3 pages.
        for i in range(15):
            add_project(title='{0}'.format(i), description='{0}'.format(i))

        url = reverse('portfolio:project_list')

        # Check buttons on first page.
        response = self.client.get(url)
        self.assertNotContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Check buttons on second page.
        response = self.client.get('{url}?page=2'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Check buttons on third page.
        response = self.client.get('{url}?page=3'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertNotContains(response, 'Next')
