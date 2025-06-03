from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    group = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    contacts = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    contacts = models.CharField(max_length=255)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# class Project(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     type = models.CharField(max_length=100)
#     status = models.CharField(max_length=100)
#     deadline = models.DateTimeField()
#     submission_date = models.DateTimeField()
#
#     def __str__(self):
#         return self.title


class ProjectAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField()

    def __str__(self):
        return f"Назначение: {self.student} → {self.teacher}, тема: {self.topic}"


class Work(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic.title} by {self.student.full_name} on {self.upload_date}"


class Grade(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    grade = models.IntegerField()
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    grade_date = models.DateTimeField()
    comments = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.work} - Grade: {self.grade}"
