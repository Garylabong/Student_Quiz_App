from django.contrib import admin

# Register your models here.
from .models import Profile, User, Category, Quiz, Question, Answer,  Student, TakenQuiz, StudentAnswer, Teacher

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name','email','is_student', 'is_teacher')
    list_filter = ("is_student","is_teacher")
    search_fields = ['first_name', 'last_name']

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)
admin.site.register(Teacher)