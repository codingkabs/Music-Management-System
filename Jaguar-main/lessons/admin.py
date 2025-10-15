from django.contrib import admin

from lessons.models import Invoice, Lesson, LessonRequest, Teacher, Term, User

# Register your models here.
admin.site.register(User)
admin.site.register(LessonRequest)
admin.site.register(Term)
admin.site.register(Teacher)
admin.site.register(Lesson)
admin.site.register(Invoice)