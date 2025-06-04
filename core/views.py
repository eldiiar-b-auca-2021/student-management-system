# views.py  –  core app
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.utils import timezone

from .models import (
    Student, Teacher, Topic, Project, Assignment, Work, Grade
)
from .forms import (
    CustomUserCreationForm, StudentForm, TeacherForm, TopicForm,
    ProjectForm, AssignmentForm, WorkForm, GradeForm
)


# ──────────────────────────────
# Small helpers
# ──────────────────────────────

def group_required(*groups):
    """Decorator that allows access only to users in given Django groups."""

    def decorator(view):
        @login_required
        @user_passes_test(lambda u: u.groups.filter(name__in=groups).exists())
        def wrapped(request, *args, **kwargs):
            return view(request, *args, **kwargs)

        return wrapped

    return decorator


# ──────────────────────────────
# Auth & Landing
# ──────────────────────────────

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            student_group, _ = Group.objects.get_or_create(name='Students')
            user.groups.add(student_group)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def home(request):
    """Dashboard cards."""
    sections = [
        {'title': 'Студенты', 'desc': 'Управление студентами', 'url': 'student_list'},
        {'title': 'Преподаватели', 'desc': 'Данные преподавателей', 'url': 'teacher_list'},
        {'title': 'Темы', 'desc': 'Темы проектов', 'url': 'topic_list'},
        {'title': 'Проекты', 'desc': 'Список проектов', 'url': 'project_list'},
        {'title': 'Назначения', 'desc': 'Кто над чем работает', 'url': 'assignment_list'},
        {'title': 'Работы', 'desc': 'Загрузки / ссылки', 'url': 'work_list'},
        {'title': 'Оценки', 'desc': 'История оценок', 'url': 'grade_list'},
    ]
    return render(request, 'core/home.html', {'sections': sections})


# ──────────────────────────────
# 1. Students
# ──────────────────────────────

@group_required('Teachers', 'Admins', 'Students')
def student_list(request):
    return render(request, 'core/student_list.html',
                  {'students': Student.objects.all()})


@group_required('Teachers', 'Admins')
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save();
        return redirect('student_list')
    return render(request, 'core/student_form.html', {'form': form})


@group_required('Teachers', 'Admins')
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save();
        return redirect('student_list')
    return render(request, 'core/student_form.html', {'form': form})


@group_required('Teachers', 'Admins')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete();
        return redirect('student_list')
    return render(request, 'core/student_confirm_delete.html', {'student': student})


# ──────────────────────────────
# 2. Teachers
# ──────────────────────────────

@group_required('Admins', 'Teachers', 'Students')
def teacher_list(request):
    return render(request, 'core/teacher_list.html',
                  {'teachers': Teacher.objects.all()})


@group_required('Admins')
def teacher_create(request):
    form = TeacherForm(request.POST or None)
    if form.is_valid():
        form.save();
        return redirect('teacher_list')
    return render(request, 'core/teacher_form.html', {'form': form})


@group_required('Admins')
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, instance=teacher)
    if form.is_valid():
        form.save();
        return redirect('teacher_list')
    return render(request, 'core/teacher_form.html', {'form': form})


@group_required('Admins')
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete();
        return redirect('teacher_list')
    return render(request, 'core/teacher_confirm_delete.html', {'teacher': teacher})


# ──────────────────────────────
# 3. Topics
# ──────────────────────────────

@group_required('Admins', 'Teachers', 'Students')
def topic_list(request):
    return render(request, 'core/topic_list.html',
                  {'topics': Topic.objects.all(),
                   'is_student': request.user.groups.filter(name='Students').exists()})


@group_required('Admins', 'Teachers')
def topic_create(request):
    form = TopicForm(request.POST or None)
    if form.is_valid():
        form.save();
        return redirect('topic_list')
    return render(request, 'core/topic_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def topic_update(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    form = TopicForm(request.POST or None, instance=topic)
    if form.is_valid():
        form.save();
        return redirect('topic_list')
    return render(request, 'core/topic_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.delete();
        return redirect('topic_list')
    return render(request, 'core/topic_confirm_delete.html', {'topic': topic})


# ──────────────────────────────
# 4. Projects
# ──────────────────────────────

@group_required('Admins', 'Teachers', 'Students')
def project_list(request):
    return render(request, 'core/project_list.html',
                  {'projects': Project.objects.all()})


@group_required('Admins', 'Teachers')
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        form.save();
        return redirect('project_list')
    return render(request, 'core/project_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save();
        return redirect('project_list')
    return render(request, 'core/project_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete();
        return redirect('project_list')
    return render(request, 'core/project_confirm_delete.html', {'project': project})


# ──────────────────────────────
# 5. Assignments   (Project ↔ Student ↔ Teacher ↔ Topic)
# ──────────────────────────────

def _assignment_queryset_for_user(user):
    """Students see своё; teachers – своё; admins – всё"""
    if user.groups.filter(name='Students').exists():
        return Assignment.objects.filter(student__user=user)
    if user.groups.filter(name='Teachers').exists():
        return Assignment.objects.filter(teacher__user=user)
    return Assignment.objects.all()


@group_required('Admins', 'Teachers', 'Students')
def assignment_list(request):
    assignments = _assignment_queryset_for_user(request.user)
    return render(request, 'core/assignment_list.html', {'assignments': assignments})


@group_required('Admins', 'Teachers')
def assignment_create(request):
    form = AssignmentForm(request.POST or None)
    if form.is_valid():
        form.save();
        return redirect('assignment_list')
    return render(request, 'core/assignment_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    form = AssignmentForm(request.POST or None, instance=assignment)
    if form.is_valid():
        form.save();
        return redirect('assignment_list')
    return render(request, 'core/assignment_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete();
        return redirect('assignment_list')
    return render(request, 'core/assignment_confirm_delete.html', {'assignment': assignment})


# ──────────────────────────────
# 6. Works   (file / link inside an assignment)
# ──────────────────────────────

def _work_queryset_for_user(user):
    if user.groups.filter(name='Students').exists():
        return Work.objects.filter(assignment__student__user=user)
    if user.groups.filter(name='Teachers').exists():
        return Work.objects.filter(assignment__teacher__user=user)
    return Work.objects.all()


@group_required('Admins', 'Teachers', 'Students')
def work_list(request):
    return render(request, 'core/work_list.html',
                  {'works': _work_queryset_for_user(request.user)})


@group_required('Admins', 'Teachers', 'Students')
def work_create(request):
    form = WorkForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        work = form.save(commit=False)
        # Stamp the student automatically if the author is a student
        if request.user.groups.filter(name='Students').exists():
            work.assignment = Assignment.objects.get(
                student__user=request.user,
                pk=request.POST.get('assignment')  # in form select
            )
        work.save()
        return redirect('work_list')
    return render(request, 'core/work_form.html', {'form': form})


@group_required('Admins', 'Teachers', 'Students')
def work_update(request, pk):
    work = get_object_or_404(Work, pk=pk)
    form = WorkForm(request.POST or None, request.FILES or None, instance=work)
    if form.is_valid():
        form.save();
        return redirect('work_list')
    return render(request, 'core/work_form.html', {'form': form})


@group_required('Admins', 'Teachers', 'Students')
def work_delete(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == 'POST':
        work.delete();
        return redirect('work_list')
    return render(request, 'core/work_confirm_delete.html', {'work': work})


# ──────────────────────────────
# 7. Grades   (Teacher evaluates Work)
# ──────────────────────────────

def _grade_queryset_for_user(user):
    if user.groups.filter(name='Students').exists():
        return Grade.objects.filter(work__assignment__student__user=user)
    if user.groups.filter(name='Teachers').exists():
        return Grade.objects.filter(graded_by__user=user)
    return Grade.objects.all()


@group_required('Admins', 'Teachers', 'Students')
def grade_list(request):
    return render(request, 'core/grade_list.html',
                  {'grades': _grade_queryset_for_user(request.user)})


@group_required('Admins', 'Teachers')
def grade_create(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        grade = form.save(commit=False)
        # Teachers: set yourself as author
        if request.user.groups.filter(name='Teachers').exists():
            grade.graded_by = Teacher.objects.get(user=request.user)
        grade.grade_date = timezone.now()
        grade.save()
        return redirect('grade_list')
    return render(request, 'core/grade_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    form = GradeForm(request.POST or None, instance=grade)
    if form.is_valid():
        form.save();
        return redirect('grade_list')
    return render(request, 'core/grade_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete();
        return redirect('grade_list')
    return render(request, 'core/grade_confirm_delete.html', {'grade': grade})
