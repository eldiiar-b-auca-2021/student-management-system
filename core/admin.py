from django.contrib import admin
from .models import Student, Teacher, Project, Topic, ProjectAssignment, Work, Grade

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'group', 'faculty')
    search_fields = ('full_name', 'group', 'faculty')
    list_filter = ('faculty',)

admin.site.register(Teacher)
admin.site.register(Project)
admin.site.register(Topic)
admin.site.register(ProjectAssignment)
admin.site.register(Work)
admin.site.register(Grade)
