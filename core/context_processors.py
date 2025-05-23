def is_student_flag(request):
    user = getattr(request, 'user', None)
    is_student = user.is_authenticated and user.groups.filter(name='Students').exists() if user else False
    return {'is_student': is_student}
