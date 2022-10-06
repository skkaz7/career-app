import pytest
from django.contrib.auth.models import User, Permission

from career_app.models import Project, WebSite, Status, Task, Company, JobOffer


@pytest.fixture()
def user_login():
    data = {
        'username': 'testowy',
        'password': 'test'
    }
    User.objects.create_user(**data)
    return data


@pytest.fixture()
def user():
    data = {
        'username': 'testowy',
        'password': 'test'
    }
    return User.objects.create_user(**data)


@pytest.fixture()
def user_with_permission_change_task():
    data = {
        'username': 'testowy',
        'password': 'test'
    }
    u = User.objects.create_user(**data)
    p = Permission.objects.get(codename='change_task')
    u.user_permissions.add(p)
    return u


@pytest.fixture()
def user_with_permission_delete_task():
    data = {
        'username': 'testowy',
        'password': 'test'
    }
    u = User.objects.create_user(**data)
    p = Permission.objects.get(codename='delete_task')
    u.user_permissions.add(p)
    return u


@pytest.fixture()
def user_with_permission_change_job_offer():
    data = {
        'username': 'testowy',
        'password': 'test'
    }
    u = User.objects.create_user(**data)
    p = Permission.objects.get(codename='change_joboffer')
    u.user_permissions.add(p)
    return u


@pytest.fixture()
def project():
    return Project.objects.create(name='python', description='programming language')


@pytest.fixture()
def projects():
    lst = []
    for x in range(10):
        p = Project()
        p.name = 'python' + str(x)
        p.description = 'programming language'
        p.save()
        lst.append(p)
    return lst


@pytest.fixture()
def website():
    return WebSite.objects.create(name='wp', link='www.wp.pl', description='strona wp')


@pytest.fixture()
def websites():
    lst = []
    for x in range(10):
        w = WebSite()
        w.name = 'wp'
        w.link = 'www.wp.pl'
        w.description = 'strona wp'
        w.save()
        lst.append(w)
    return lst


@pytest.fixture()
def status():
    return Status.objects.create(status_name='to do')


@pytest.fixture()
def task(project, website, status):
    return Task.objects.create(name='test', description='test', estimated_time=10, difficulty=1, category='test',
                               slug='test', deadline='2022-08-28', status=status, website=website,
                               project=project)


@pytest.fixture()
def tasks(project, website, status):
    lst = []
    for x in range(10):
        t = Task()
        t.name = 'test'
        t.description = 'test'
        t.estimated_time = 10
        t.difficulty = 1
        t.category = 'test'
        t.slug = 'test' + str(x)
        t.deadline = '2022-08-31'
        t.status = status
        t.website = website
        t.project = project
        t.save()
        lst.append(t)
    return lst


@pytest.fixture()
def job_offer(company, website):
    return JobOffer.objects.create(company=company, position='test', city='test', received='2022-08-28', is_active=True,
                                   min_salary=10, max_salary=100, type_of_contract=1, benefits='test',
                                   requirements='test', website=website)


@pytest.fixture()
def job_offers(company, website):
    lst = []
    for x in range(10):
        j = JobOffer()
        j.company = company
        j.position = 'test'
        j.city = 'test'
        j.received = '2022-08-28'
        j.is_active = True
        j.min_salary = 10
        j.max_salary = 100
        j.type_of_contract = 1
        j.benefits = 'test'
        j.requirements = 'test'
        j.website = website
        j.save()
        lst.append(j)
    return lst


@pytest.fixture()
def company():
    return Company.objects.create(name='test', description='test test')


@pytest.fixture()
def companies():
    lst = []
    for x in range(10):
        c = Company()
        c.name = 'test'
        c.description = 'test test'
        c.save()
        lst.append(c)
    return lst
