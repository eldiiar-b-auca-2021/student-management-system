from django import forms
from .models import Student, Teacher, Topic, ProjectAssignment, Work, Grade
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        labels = {
            'full_name': 'Полное имя',
            'group': 'Группа',
            'faculty': 'Факультет',
            'contacts': 'Контакты',
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        labels = {
            'full_name': 'Полное имя',
            'contacts': 'Контакты',
            'department': 'Кафедра',
        }

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = '__all__'
#         labels = {
#             'title': 'Название проекта',
#             'description': 'Описание',
#             'type': 'Тип проекта',
#             'status': 'Статус',
#             'deadline': 'Крайний срок',
#             'submission_date': 'Дата сдачи',
#         }
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название проекта'}),
#             'description': forms.Textarea(
#                 attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание проекта'}),
#             'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тип проекта'}),
#             'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Статус проекта'}),
#             'deadline': forms.DateTimeInput(attrs={
#                 'class': 'form-control',
#                 'type': 'datetime-local',
#                 'placeholder': 'Крайний срок'
#             }),
#             'submission_date': forms.DateTimeInput(attrs={
#                 'class': 'form-control',
#                 'type': 'datetime-local',
#                 'placeholder': 'Дата сдачи'
#             }),
#         }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
        labels = {
            'title': 'Название темы',
            'description': 'Описание',
            'is_active': 'Активна',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название темы'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите описание'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        exclude = ['project']
        labels = {
            'student': 'Студент',
            'teacher': 'Преподаватель',
            'topic': 'Тема',
            'assigned_date': 'Дата назначения',
        }
        widgets = {
            'assigned_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),

        }


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'
        labels = {
            # 'project': 'Проект',
            'file_path': 'Путь к файлу',
            'link': 'Ссылка на работу',
            'upload_date': 'Дата загрузки',
        }
        widgets = {
            'upload_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'
        labels = {
            # 'project': 'Проект',
            'grade': 'Оценка',
            'graded_by': 'Оценил',
            'grade_date': 'Дата оценки',
            'comments': 'Комментарии',
        }
        widgets = {
            'grade_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
