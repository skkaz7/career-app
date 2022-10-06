from django.db import models

DIFFICULTY = (
    (1, "Łatwe"),
    (2, "średnie"),
    (3, "Trudne")
)


class Status(models.Model):
    status_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.status_name}"


class WebSite(models.Model):
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=64)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    estimated_time = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    difficulty = models.IntegerField(choices=DIFFICULTY)
    category = models.CharField(max_length=64)
    slug = models.CharField(max_length=64, unique=True)
    deadline = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    website = models.ForeignKey(WebSite, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parent = models.ForeignKey("Task", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    # is_interested = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


TYPE_OF_CONTRACT = (
    (1, "Umowa o pracę"),
    (2, "B2B"),
    (3, "Umowa zlecenie"),
    (4, "Umowa o dzieło")
)


class JobOffer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    received = models.DateField()
    is_active = models.BooleanField(default=True)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    type_of_contract = models.IntegerField(choices=TYPE_OF_CONTRACT)
    benefits = models.TextField()
    requirements = models.TextField()
    website = models.ForeignKey(WebSite, on_delete=models.CASCADE)
