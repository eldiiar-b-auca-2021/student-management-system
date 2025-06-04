# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    Student, Teacher, Topic, Project, Assignment, Work, Grade
)

# ───────────────────────────────
# 1. Auth
# ───────────────────────────────
class CustomUserCreationForm(UserCreationForm):
    """Подчистили help-text, оставили только username / password."""
    class Meta:
        model  = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ['username', 'password1', 'password2']:
            self.fields[f].help_text = None
            self.fields[f].widget.attrs.update({'class': 'form-control'})


# ───────────────────────────────
# 2. Core directory (students / teachers)
# ───────────────────────────────
def _bootstrap(form):
    """Маленький миксин для единого оформления."""
    for field in form.fields.values():
        if not isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault('class', 'form-control')
    return form

class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        exclude = ('user',)            # user связываем отдельно
        labels = {
            'full_name': 'Полное имя',
            'group':     'Группа',
            'faculty':   'Факультет',
            'contacts':  'Контакты',
        }
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); _bootstrap(self)

class TeacherForm(forms.ModelForm):
    class Meta:
        model  = Teacher
        exclude = ('user',)
        labels = {
            'full_name':  'Полное имя',
            'department': 'Кафедра',
            'contacts':   'Контакты',
        }
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); _bootstrap(self)


# ───────────────────────────────
# 3. Topic
# ───────────────────────────────
class TopicForm(forms.ModelForm):
    class Meta:
        model  = Topic
        fields = '__all__'
        labels = {
            'title':       'Название темы',
            'description': 'Описание',
            'is_active':   'Активна',
        }
        widgets = {
            'title':       forms.TextInput(attrs={'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите описание'}),
            'is_active':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); _bootstrap(self)


# ───────────────────────────────
# 4. Project
# ───────────────────────────────
class ProjectForm(forms.ModelForm):
    class Meta:
        model  = Project
        fields = ('title', 'description', 'type', 'status', 'deadline')
        labels = {
            'title':       'Название проекта',
            'description': 'Описание',
            'type':        'Тип',
            'status':      'Статус',
            'deadline':    'Крайний срок',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'deadline':    forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); _bootstrap(self)


# ───────────────────────────────
# 5. Assignment  (student ↔ project)
# ───────────────────────────────
class AssignmentForm(forms.ModelForm):
    class Meta:
        model  = Assignment
        fields = ('student', 'teacher', 'project', 'topic', 'assigned_date')
        labels = {
            'student':       'Студент',
            'teacher':       'Преподаватель',
            'project':       'Проект',
            'topic':         'Тема',
            'assigned_date': 'Дата назначения',
        }
        widgets = {
            'assigned_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); _bootstrap(self)
        # Показываем только активные темы
        self.fields['topic'].queryset = Topic.objects.filter(is_active=True)


# ───────────────────────────────
# 6. Work   (file || link)
# ───────────────────────────────
class WorkForm(forms.ModelForm):
    class Meta:
        model  = Work
        fields = ('assignment', 'title', 'file', 'link')
        labels = {
            'assignment': 'Назначение',
            'title':      'Название работы',
            'file':       'Файл',
            'link':       'Ссылка',
        }
        widgets = {
            'link': forms.URLInput(attrs={'placeholder': 'https://…'}),
        }
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); _bootstrap(self)

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('file') and not cleaned.get('link'):
            raise forms.ValidationError('Нужно загрузить файл или указать ссылку.')
        return cleaned


# ───────────────────────────────
# 7. Grade  (teacher evaluates work)
# ───────────────────────────────
class GradeForm(forms.ModelForm):
    """`graded_by` и `grade_date` заполняются во view, поэтому скрываем."""
    class Meta:
        model  = Grade
        fields = ('work', 'grade', 'comments')
        labels = {
            'work':     'Работа',
            'grade':    'Оценка',
            'comments': 'Комментарий',
        }
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); _bootstrap(self)
