from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
import datetime

from career_app.models import Task, Project, Status, WebSite, Company, JobOffer
from projekt_koncowy_django.forms import TaskForm, JobOfferForm


class Base(View):
    def get(self, request):
        task_counter = Task.objects.count()
        project_counter = Project.objects.count()
        job_offer_counter = JobOffer.objects.filter(is_active=True).count()
        task = Task.objects.last()
        project = Project.objects.last()
        job_offer = JobOffer.objects.last()
        return render(request, 'base2.html', {'user': request.user,
                                              'task': task,
                                              'task_counter': task_counter,
                                              'project': project,
                                              'project_counter': project_counter,
                                              'job_offer': job_offer,
                                              'job_offer_counter': job_offer_counter})


# class AddTaskView(LoginRequiredMixin, CreateView):
#     model = Task
#     template_name = 'add_task.html'
#     fields = '__all__'
#     success_url = reverse_lazy('add_task')

class AddTaskView(LoginRequiredMixin, View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'add_task.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            slug = slugify(name)
            form.cleaned_data['slug'] = slug
            Task.objects.create(**form.cleaned_data)
        return redirect(reverse('task_list'))


class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(TaskListView, self).get_context_data()
        today = datetime.date.today().day
        data.update({'today': today})
        return data


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_details.html'

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     children = Task.objects.all()
    #     data.update({'children': children})
    #     return data


class AddProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'add_project.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('project_list')


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'


class AddStatusView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'add_status.html'
    fields = '__all__'
    success_url = reverse_lazy('add_status')


class AddWebsiteView(LoginRequiredMixin, CreateView):
    model = WebSite
    template_name = 'add_website.html'
    fields = '__all__'
    success_url = reverse_lazy('website_list')


class WebsiteListView(ListView):
    model = WebSite
    template_name = 'website_list.html'


class TaskUpdateView(PermissionRequiredMixin, View):
    permission_required = ['career_app.change_task']

    def get(self, request, slug):
        task_to_update = Task.objects.get(slug=slug)
        form = TaskForm(instance=task_to_update)
        return render(request, 'add_task.html', {'form': form})

    def post(self, request, slug):
        task_to_update = Task.objects.get(slug=slug)
        form = TaskForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['name']
            new_description = form.cleaned_data['description']
            new_estimated_time = form.cleaned_data['estimated_time']
            new_difficulty = form.cleaned_data['difficulty']
            new_category = form.cleaned_data['category']
            new_deadline = form.cleaned_data['deadline']
            new_status = form.cleaned_data['status']
            new_website = form.cleaned_data['website']
            new_project = form.cleaned_data['project']
            new_slug = slugify(new_name)
            task_to_update.name = new_name
            task_to_update.description = new_description
            task_to_update.estimated_time = new_estimated_time
            task_to_update.difficulty = new_difficulty
            task_to_update.category = new_category
            task_to_update.deadline = new_deadline
            task_to_update.status = new_status
            task_to_update.website = new_website
            task_to_update.project = new_project
            task_to_update.slug = new_slug
            task_to_update.save()
            return redirect(reverse('task_list'))


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['career_app.delete_task']
    model = Task
    template_name = 'delete_task.html'
    success_url = reverse_lazy('task_list')


class AddCompanyView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'add_company.html'
    fields = '__all__'
    success_url = reverse_lazy('company_list')


class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'


class AddJobOfferView(LoginRequiredMixin, View):
    def get(self, request):
        form = JobOfferForm()
        return render(request, 'add_job_offer.html', {'form': form})

    def post(self, request):
        form = JobOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('job_offer_list'))


class JobOfferListView(ListView):
    model = JobOffer
    template_name = 'job_offer_list.html'


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_details.html'


class JobOfferUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['career_app.change_joboffer']
    model = JobOffer
    fields = '__all__'
    template_name = 'job_offer_update.html'
    success_url = reverse_lazy('job_offer_list')
