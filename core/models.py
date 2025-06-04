# app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, blank=True)
    full_name = models.CharField('ФИО', max_length=255)
    group = models.CharField('Группа', max_length=100, blank=True)
    faculty = models.CharField('Факультет', max_length=100, blank=True)
    contacts = models.CharField('Контакты', max_length=255, blank=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, blank=True)
    full_name = models.CharField('ФИО', max_length=255)
    department = models.CharField('Кафедра', max_length=100, blank=True)
    contacts = models.CharField('Контакты', max_length=255, blank=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Topic(models.Model):
    title = models.CharField('Название темы', max_length=255)
    description = models.TextField('Описание')
    is_active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    class ProjectType(models.TextChoices):
        DIPLOMA = 'diploma', 'Дипломный'
        COURSE = 'course', 'Курсовой'
        RESEARCH = 'research', 'Научный'

    class ProjectStatus(models.TextChoices):
        NEW = 'new', 'Новый'
        IN_PROGRESS = 'progress', 'В работе'
        COMPLETED = 'done', 'Завершён'

    title = models.CharField('Проект', max_length=255)
    description = models.TextField('Описание')
    type = models.CharField('Тип', max_length=20,
                            choices=ProjectType.choices)
    status = models.CharField('Статус', max_length=20,
                              choices=ProjectStatus.choices,
                              default=ProjectStatus.NEW)
    deadline = models.DateTimeField('Дедлайн', null=True, blank=True)
    submission_date = models.DateTimeField('Фактическая сдача',
                                           null=True, blank=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    """
    Назначение конкретного проекта студенту + кураторам / теме.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name='assignments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='assignments')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='assignments')
    assigned_date = models.DateTimeField('Дата назначения',
                                         default=timezone.now)

    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'
        unique_together = ('student', 'project')  # 1-студент-1-проект

    def __str__(self):
        return f"{self.student} → {self.project} (преп. {self.teacher})"


class Work(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='works')
    title = models.CharField('Название работы', max_length=255, blank=True)
    link = models.URLField('Ссылка', max_length=500)  # required now
    upload_date = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.assignment.project.title} – {self.assignment.student}"


class Grade(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE,
                             related_name='grades')
    grade = models.PositiveSmallIntegerField('Оценка')
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL,
                                  null=True, related_name='given_grades')
    grade_date = models.DateTimeField('Когда выставлена',
                                      default=timezone.now)
    comments = models.CharField('Комментарий', max_length=500, blank=True)

    class Meta:
        ordering = ['-grade_date']

    def __str__(self):
        return f"{self.work} → {self.grade}"
