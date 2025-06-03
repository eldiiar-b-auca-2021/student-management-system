# views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Topic, ProjectAssignment, Work, Grade, Student, Teacher
from .forms import TopicForm, ProjectAssignmentForm, WorkForm, GradeForm, StudentForm, TeacherForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from functools import wraps


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            student_group, created = Group.objects.get_or_create(name='Students')
            user.groups.add(student_group)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def home(request):
    sections = [
        {'title': 'Студенты', 'desc': 'Управление всеми записями студентов.', 'url': 'student_list'},
        {'title': 'Преподаватели', 'desc': 'Управление данными преподавателей и контактами.', 'url': 'teacher_list'},
        {'title': 'Темы', 'desc': 'Просмотр и управление темами проектов.', 'url': 'topic_list'},
        {'title': 'Назначения', 'desc': 'Просмотр назначений проектов студентам.', 'url': 'assignment_list'},
        {'title': 'Оценки', 'desc': 'История оценивания проектов.', 'url': 'grade_list'},
        {'title': 'Работы', 'desc': 'Загруженные файлы и ссылки на проекты.', 'url': 'work_list'},
    ]
    return render(request, 'core/home.html', {'sections': sections})


def group_required(*group_names):
    def decorator(view_func):
        @login_required
        @user_passes_test(lambda u: u.groups.filter(name__in=group_names).exists())
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# @group_required('Admins', 'Teachers', 'Students')
# def project_list(request):
#     projects = Project.objects.all()
#     return render(request, 'core/project_list.html', {'projects': projects})


# @group_required('Admins', 'Teachers', 'Students')
# def project_create(request):
#     form = ProjectForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('project_list')
#     return render(request, 'core/project_form.html', {'form': form})
#

# @group_required('Admins', 'Teachers', 'Students')
# def project_update(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     form = ProjectForm(request.POST or None, instance=project)
#     if form.is_valid():
#         form.save()
#         return redirect('project_list')
#     return render(request, 'core/project_form.html', {'form': form})
#

# @group_required('Admins', 'Teachers', 'Students')
# def project_delete(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     if request.method == 'POST':
#         project.delete()
#         return redirect('project_list')
#     return render(request, 'core/project_confirm_delete.html', {'project': project})


@group_required('Admins', 'Teachers', 'Students')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/student_list.html', {'students': students})


@group_required('Teachers', 'Admins')
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'core/student_form.html', {'form': form})


@group_required('Teachers', 'Admins')
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'core/student_form.html', {'form': form})


@group_required('Teachers', 'Admins')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'core/student_confirm_delete.html', {'student': student})


@group_required('Teachers', 'Admins', 'Students')
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'core/teacher_list.html', {'teachers': teachers})


@group_required('Admins')
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'core/teacher_form.html', {'form': form})


@group_required('Admins')
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'core/teacher_form.html', {'form': form})


@group_required('Admins')
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'core/teacher_confirm_delete.html', {'teacher': teacher})


# TOPIC CRUD

@group_required('Admins', 'Teachers', 'Students')
def topic_list(request):
    topics = Topic.objects.all()
    is_student = request.user.groups.filter(name='Students').exists()
    return render(request, 'core/topic_list.html', {
        'topics': topics,
        'is_student': is_student
    })


@group_required('Admins', 'Teachers')
def topic_create(request):
    form = TopicForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('topic_list')
    return render(request, 'core/topic_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def topic_update(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    form = TopicForm(request.POST or None, instance=topic)
    if form.is_valid():
        form.save()
        return redirect('topic_list')
    return render(request, 'core/topic_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.delete()
        return redirect('topic_list')
    return render(request, 'core/topic_confirm_delete.html', {'topic': topic})


@group_required('Admins', 'Teachers', 'Students')
def assignment_list(request):
    assignments = ProjectAssignment.objects.all()
    return render(request, 'core/assignment_list.html', {'assignments': assignments})


@group_required('Admins', 'Teachers')
def assignment_create(request):
    form = ProjectAssignmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('assignment_list')
    return render(request, 'core/assignment_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def assignment_update(request, pk):
    assignment = get_object_or_404(ProjectAssignment, pk=pk)
    form = ProjectAssignmentForm(request.POST or None, instance=assignment)
    if form.is_valid():
        form.save()
        return redirect('assignment_list')
    return render(request, 'core/assignment_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def assignment_delete(request, pk):
    assignment = get_object_or_404(ProjectAssignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')
    return render(request, 'core/assignment_confirm_delete.html', {'assignment': assignment})


# WORK CRUD
@group_required('Admins', 'Teachers', 'Students')
def work_list(request):
    works = Work.objects.all()
    return render(request, 'core/work_list.html', {'works': works})


@group_required('Admins', 'Teachers', 'Students')
def work_create(request):
    form = WorkForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('work_list')
    return render(request, 'core/work_form.html', {'form': form})


@group_required('Admins', 'Teachers', 'Students')
def work_update(request, pk):
    work = get_object_or_404(Work, pk=pk)
    form = WorkForm(request.POST or None, instance=work)
    if form.is_valid():
        form.save()
        return redirect('work_list')
    return render(request, 'core/work_form.html', {'form': form})


@group_required('Admins', 'Teachers', 'Students')
def work_delete(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == 'POST':
        work.delete()
        return redirect('work_list')
    return render(request, 'core/work_confirm_delete.html', {'work': work})


# GRADE CRUD

@group_required('Admins', 'Teachers', 'Students')
def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'core/grade_list.html', {'grades': grades})


@group_required('Admins', 'Teachers')
def grade_create(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('grade_list')
    return render(request, 'core/grade_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    form = GradeForm(request.POST or None, instance=grade)
    if form.is_valid():
        form.save()
        return redirect('grade_list')
    return render(request, 'core/grade_form.html', {'form': form})


@group_required('Admins', 'Teachers')
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grade_list')
    return render(request, 'core/grade_confirm_delete.html', {'grade': grade})
