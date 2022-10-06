import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from accounts.forms import LoginForm, ChangePasswordForm, CreateUserForm
from projekt_koncowy_django.forms import TaskForm, JobOfferForm
from career_app.models import Task, Project, Status, WebSite, Company, JobOffer

"""
INDEX + BASE
"""


def test_index(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_base(client):
    url = reverse('base')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_base_template(client):
    url = reverse('base')
    response = client.get(url)
    assertTemplateUsed(response, 'base2.html')
    assertContains(response, 'task')


"""
TESTY NA LOGIN VIEW
"""


def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, LoginForm)


@pytest.mark.django_db
def test_login_view_post(client, user_login):
    url = reverse('login')
    response = client.post(url, user_login)
    assert response.status_code == 302
    assert response.url == reverse('base')


@pytest.mark.django_db
def test_login_view_post_next(client, user_login):
    url = reverse('login')
    url += "?next=" + reverse('add_task')
    response = client.post(url, user_login)
    assert response.status_code == 302
    assert response.url == reverse('add_task')


"""
TESTY NA LOGOUT
"""


@pytest.mark.django_db
def test_logout_view_get(client, user):
    url = reverse('logout')
    client.force_login(user)
    response = client.get(url)
    client.logout()
    assert response.status_code == 302
    assert response.url.startswith(reverse('base'))


"""
TESTY NA CHANGE PASSWORD VIEW
"""


def test_change_password_get(client):
    url = reverse('change_password')
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, ChangePasswordForm)


@pytest.mark.django_db
def test_change_password_post(client, user):
    url = reverse('change_password')
    client.force_login(user)
    new_pass = {
        'old_password': 'test',
        'new_password': 'test2',
        're_new_password': 'test2'
    }
    response = client.post(url, new_pass)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


"""
TESTY NA REGISTER VIEW
"""


def test_register_view_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, CreateUserForm)


@pytest.mark.django_db
def test_register_view_post(client):
    url = reverse('register')
    new_user = {
        'username': 'testu',
        'password': 'testp',
        're_password': 'testp'
    }
    response = client.post(url, new_user)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    assert User.objects.get(username=new_user['username'])


"""
TESTY ADD TASK VIEW
"""


def test_add_task_view_get_no_login(client):
    url = reverse('add_task')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_task_view_get_login(client, user):
    url = reverse('add_task')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, TaskForm)


@pytest.mark.django_db
def test_add_task_view_post_login(client, user, project, website, status):
    url = reverse('add_task')
    data = {
        'name': 'test',
        'description': 'test',
        'estimated_time': 10,
        'difficulty': 1,
        'category': 'test',
        'slug': 'test',
        'deadline': '2022-08-28',
        'status': status.id,
        'website': website.id,
        'project': project.id
    }
    client.force_login(user)
    response = client.post(url, data)
    assert response.status_code == 302
    assert Task.objects.get(**data)
    assert response.url == reverse('task_list')


"""
TESTY NA ADD PROJECT VIEW
"""


def test_add_project_view_get_no_login(client):
    url = reverse('add_project')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_project_view_get_login(client, user):
    url = reverse('add_project')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_project_view_post_login(client, user):
    url = reverse('add_project')
    data = {
        'name': 'test',
        'description': 'test'
    }
    client.force_login(user)
    response = client.post(url, data)
    assert response.status_code == 302
    assert Project.objects.get(**data)
    assert response.url == reverse('project_list')


"""
TESTY NA TASK LIST VIEW
"""


@pytest.mark.django_db
def test_task_list_view(client, tasks):
    url = reverse('task_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(tasks)
    for task in tasks:
        assert task in response.context['object_list']


@pytest.mark.django_db
def test_task_list_view_template(client):
    url = reverse('task_list')
    response = client.get(url)
    assertTemplateUsed(response, 'task_list.html')
    assertContains(response, 'task')


"""
TESTY NA TASK DETAIL VIEW
"""


@pytest.mark.django_db
def test_task_detail_view(client, task):
    url = reverse('task_details', kwargs={'slug': task.slug})
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'task_details.html')


@pytest.mark.django_db
def test_task_detail_view_template(client, task):
    url = reverse('task_details', kwargs={'slug': task.slug})
    response = client.get(url)
    assertTemplateUsed(response, 'task_details.html')
    assertContains(response, 'task')


"""
TESTY NA PROJECT LIST VIEW
"""


@pytest.mark.django_db
def test_project_list_view(client, projects):
    url = reverse('project_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(projects)
    for project in projects:
        assert project in response.context['object_list']


@pytest.mark.django_db
def test_project_list_view_template(client):
    url = reverse('project_list')
    response = client.get(url)
    assertTemplateUsed(response, 'project_list.html')
    assertContains(response, 'project')


"""
TESTY NA ADD STATUS VIEW
"""


def test_add_status_get_no_login(client):
    url = reverse('add_status')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_status_get_login(client, user):
    url = reverse('add_status')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_status_post_login(client, user):
    url = reverse('add_status')
    data = {
        'status_name': 'test'
    }
    client.force_login(user)
    response = client.post(url, data)
    assert response.status_code == 302
    assert Status.objects.get(**data)
    assert response.url == reverse('add_status')


"""
TESTY NA ADD WEBSITE VIEW
"""


def test_add_website_get_no_login(client):
    url = reverse('add_website')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_website_get_login(client, user):
    url = reverse('add_website')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_website_post_login(client, user):
    url = reverse('add_website')
    data = {
        'name': 'test',
        'link': 'www.test.com',
        'description': 'test'
    }
    client.force_login(user)
    response = client.post(url, data)
    assert response.status_code == 302
    assert WebSite.objects.get(**data)
    assert response.url == reverse('website_list')


"""
TESTY NA WEBSITE LIST VIEW
"""


@pytest.mark.django_db
def test_website_list_view(client, websites):
    url = reverse('website_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(websites)
    for website in websites:
        assert website in response.context['object_list']


@pytest.mark.django_db
def test_website_list_view_template(client):
    url = reverse('website_list')
    response = client.get(url)
    assertTemplateUsed(response, 'website_list.html')
    assertContains(response, 'website')


"""
TESTY NA TASK UPDATE VIEW
"""


class TestTaskUpdateView:
    @pytest.mark.django_db
    def test_task_update_view_no_login(self, client, task):
        url = reverse('task_update', kwargs={'slug': task.slug})
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    @pytest.mark.django_db
    def test_task_update_view_no_permission(self, client, user, task):
        url = reverse('task_update', kwargs={'slug': task.slug})
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_task_update_view_get(self, client, user_with_permission_change_task, task):
        url = reverse('task_update', kwargs={'slug': task.slug})
        client.force_login(user_with_permission_change_task)
        response = client.get(url)
        assert response.status_code == 200
        form = response.context['form']
        assert isinstance(form, TaskForm)

    @pytest.mark.django_db
    def test_task_update_view_post(self, client, user_with_permission_change_task, task, status, website, project):
        url = reverse('task_update', kwargs={'slug': task.slug})
        data = {
            'name': 'test2',
            'description': 'test',
            'estimated_time': 10,
            'difficulty': 1,
            'category': 'test',
            'slug': 'test',
            'deadline': '2022-08-28',
            'status': status.id,
            'website': website.id,
            'project': project.id
        }
        client.force_login(user_with_permission_change_task)
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('task_list')


"""
TESTY NA TASK DELETE VIEW
"""


class TestTaskDeleteView:
    @pytest.mark.django_db
    def test_task_delete_view_no_login(self, client, task):
        url = reverse('task_delete', kwargs={'slug': task.slug})
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    @pytest.mark.django_db
    def test_task_delete_view_no_permission(self, client, user, task):
        url = reverse('task_delete', kwargs={'slug': task.slug})
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_task_delete_view_get(self, client, user_with_permission_delete_task, task):
        url = reverse('task_delete', kwargs={'slug': task.slug})
        client.force_login(user_with_permission_delete_task)
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_task_delete_view_post(self, client, user_with_permission_delete_task, task, status, website, project):
        url = reverse('task_delete', kwargs={'slug': task.slug})
        client.force_login(user_with_permission_delete_task)
        response = client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('task_list')


"""
TESTY NA ADD COMPANY VIEW
"""


class TestAddCompanyView:
    def test_add_company_get_no_login(self, client):
        url = reverse('add_company')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    @pytest.mark.django_db
    def test_add_company_get_login(self, client, user):
        url = reverse('add_company')
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_add_company_post_login(self, client, user):
        url = reverse('add_company')
        data = {
            'name': 'test_company',
            'description': 'test_description'
        }
        client.force_login(user)
        response = client.post(url, data)
        assert response.status_code == 302
        assert Company.objects.get(**data)
        assert response.url == reverse('company_list')


"""
TESTY NA COMPANY LIST VIEW
"""


@pytest.mark.django_db
def test_companies_list_view(client, companies):
    url = reverse('company_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(companies)
    for company in companies:
        assert company in response.context['object_list']


@pytest.mark.django_db
def test_companies_list_view_template(client):
    url = reverse('company_list')
    response = client.get(url)
    assertTemplateUsed(response, 'company_list.html')
    assertContains(response, 'company')


"""
TESTY ADD JOB OFFER VIEW
"""


class TestAddJobOfferView:
    def test_add_job_offer_view_get_no_login(self, client):
        url = reverse('add_job_offer')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    @pytest.mark.django_db
    def test_add_job_offer_view_get_login(self, client, user):
        url = reverse('add_job_offer')
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == 200
        form = response.context['form']
        assert isinstance(form, JobOfferForm)

    @pytest.mark.django_db
    def test_add_job_offer_view_post_login(self, client, user, company, website):
        url = reverse('add_job_offer')
        data = {
            'company': company.id,
            'position': 'test',
            'city': 'test',
            'received': '2022-08-28',
            'is_active': True,
            'min_salary': 1000,
            'max_salary': 10000,
            'type_of_contract': 1,
            'benefits': 'test',
            'requirements': 'test',
            'website': website.id
        }
        client.force_login(user)
        response = client.post(url, data)
        assert response.status_code == 302
        assert JobOffer.objects.get(**data)
        assert response.url == reverse('job_offer_list')


"""
TESTY NA JOB OFFER LIST VIEW
"""


@pytest.mark.django_db
def test_job_offer_list_view(client, job_offers):
    url = reverse('job_offer_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(job_offers)
    for job_offer in job_offers:
        assert job_offer in response.context['object_list']


@pytest.mark.django_db
def test_job_offer_list_view_template(client):
    url = reverse('job_offer_list')
    response = client.get(url)
    assertTemplateUsed(response, 'job_offer_list.html')
    assertContains(response, 'job offer')


"""
TESTY NA COMPANY DETAIL VIEW
"""


@pytest.mark.django_db
def test_company_detail_view(client, company):
    url = reverse('company_details', kwargs={'pk': company.pk})
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'company_details.html')


@pytest.mark.django_db
def test_company_detail_view_template(client, company):
    url = reverse('company_details', kwargs={'pk': company.pk})
    response = client.get(url)
    assertTemplateUsed(response, 'company_details.html')
    assertContains(response, 'company')


"""
TESTY NA JOB OFFER UPDATE VIEW
"""


class TestJobOfferUpdateView:
    @pytest.mark.django_db
    def test_job_offer_update_view_no_login(self, client, job_offer):
        url = reverse('job_offer_update', kwargs={'pk': job_offer.pk})
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    @pytest.mark.django_db
    def test_job_offer_update_view_no_permission(self, client, user, job_offer):
        url = reverse('job_offer_update', kwargs={'pk': job_offer.pk})
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_job_offer_update_view_get(self, client, user_with_permission_change_job_offer, job_offer):
        url = reverse('job_offer_update', kwargs={'pk': job_offer.pk})
        client.force_login(user_with_permission_change_job_offer)
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_job_offer_update_view_post(self, client, user_with_permission_change_job_offer, job_offer, company,
                                        website):
        url = reverse('job_offer_update', kwargs={'pk': job_offer.pk})
        data = {
            'company': company.id,
            'position': 'test2',
            'city': 'test2',
            'received': '2022-08-28',
            'is_active': True,
            'min_salary': 10,
            'max_salary': 100,
            'type_of_contract': 1,
            'benefits': 'test2',
            'requirements': 'test2',
            'website': website.id
        }
        client.force_login(user_with_permission_change_job_offer)
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('job_offer_list')
