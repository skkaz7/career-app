from datetime import datetime
from django import forms

from career_app.models import Task, DIFFICULTY, Status, JobOffer, TYPE_OF_CONTRACT


class TaskForm(forms.ModelForm):
    difficulty = forms.ChoiceField(choices=DIFFICULTY, widget=forms.RadioSelect())
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    estimated_time = forms.IntegerField(help_text="W minutach", widget=forms.NumberInput(attrs={'min': 1}))

    class Meta:
        model = Task
        exclude = ['slug']


class JobOfferForm(forms.ModelForm):
    type_of_contract = forms.ChoiceField(choices=TYPE_OF_CONTRACT, widget=forms.RadioSelect())
    received = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    min_salary = forms.IntegerField(help_text="W złotych", widget=forms.NumberInput(attrs={'min': 0}))
    max_salary = forms.IntegerField(help_text="W złotych", widget=forms.NumberInput(attrs={'min': 0}))

    class Meta:
        model = JobOffer
        fields = '__all__'
