from django import forms
from .models import Student, Teacher, Project, Topic, ProjectAssignment, Work, Grade

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class ProjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = '__all__'

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'
