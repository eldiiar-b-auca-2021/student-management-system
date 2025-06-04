# core/admin.py
from django.contrib import admin
from .models import (
    Student, Teacher, Topic, Project, Assignment, Work, Grade
)


# ─────────────────────────
# 1. Students & Teachers
# ─────────────────────────
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group', 'faculty')
    search_fields = ('full_name', 'group', 'faculty')
    list_filter = ('faculty',)
    ordering = ('full_name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'contacts')
    search_fields = ('full_name', 'department')
    list_filter = ('department',)
    ordering = ('full_name',)


# ─────────────────────────
# 2. Topic
# ─────────────────────────
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)
    ordering = ('title',)


# ─────────────────────────
# 3. Project
# ─────────────────────────
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'deadline', 'submission_date')
    list_filter = ('type', 'status')
    search_fields = ('title',)
    date_hierarchy = 'deadline'
    ordering = ('status', 'deadline')


# ─────────────────────────
# 4. Assignment  (Student ↔ Project)
# ─────────────────────────
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'project', 'teacher', 'topic', 'assigned_date')
    list_filter = ('teacher', 'project__status', 'topic')
    search_fields = (
        'student__full_name',
        'project__title',
        'teacher__full_name',
    )
    autocomplete_fields = ('student', 'teacher', 'project', 'topic')
    date_hierarchy = 'assigned_date'


# ─────────────────────────
# 5. Work
# ─────────────────────────
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'title', 'has_file', 'has_link', 'upload_date')
    list_filter = ('assignment__project', 'upload_date')
    search_fields = ('assignment__student__full_name', 'title')
    date_hierarchy = 'upload_date'
    autocomplete_fields = ('assignment',)

    @admin.display(boolean=True, description='Файл')
    def has_file(self, obj):
        return bool(obj.file)

    @admin.display(boolean=True, description='Ссылка')
    def has_link(self, obj):
        return bool(obj.link)


# ─────────────────────────
# 6. Grade
# ─────────────────────────
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('work', 'grade', 'graded_by', 'grade_date')
    list_filter = ('grade', 'graded_by')
    search_fields = (
        'work__assignment__student__full_name',
        'work__assignment__project__title',
    )
    date_hierarchy = 'grade_date'
    autocomplete_fields = ('work', 'graded_by')
