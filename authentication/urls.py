from django.urls import include, path

from .views import classroom, students, teachers
from . import views
from .views.classroom import *

urlpatterns = [
path('token/' , token_send , name="token_send"),
path('success/' , success , name='success'),
path('verify/<auth_token>' , verify , name="verify"),
path('error/' , error_page , name="error"),
path('change_password/', classroom.change_password, name='change_password'),
path('edit_profile/',classroom.edit_profile, name="edit_profile"),
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.S_dashboard, name='S_dashboard'),
        path('quiz_list', students.QuizListView.as_view(), name='quiz_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.T_dashboard, name='T_dashboard'),
        path('quiz_add_category', teachers.QuizAddCategoryView.as_view(), name='quiz_add_category'),
        path('quiz_change_list', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]