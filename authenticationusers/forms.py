from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import (Answer, Question, Student, StudentAnswer, Teacher,
                              Category, User)


class StudentSignUpForm(UserCreationForm):
	email       = forms.EmailField(label="", widget=forms. TextInput(attrs={'class':'form-control', 'placeholder': 'Email Address'}))
#	first_name  = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}))
#	last_name   = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))
	interests = forms.ModelMultipleChoiceField(
		queryset=Category.objects.all(),
    	widget=forms.CheckboxSelectMultiple,
    	required=True)

	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.email=self.cleaned_data.get('email')
		user.is_student = True
		user.save()
		student = Student.objects.create(user=user)
		student.interests.add(*self.cleaned_data.get('interests'))
		return user

class TeacherSignUpForm(UserCreationForm):
    email       = forms.EmailField(label="", widget=forms. TextInput(attrs={'class':'form-control', 'placeholder': 'Email Address'}))
#    first_name  = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}))
#    last_name   = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))
  
    class Meta(UserCreationForm.Meta):
        model = User

    #@transaction.atomic
    #def save(self):
    #    user = super().save(commit=False)
    #    user.email=self.cleaned_data.get('email')
    #    user.is_teacher = True
    #    user.save()
    #    teacher = Teacher.objects.create(user=user)
    #
    #    teacher.save()
    #
    #    return teacher
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_teacher = True
        if commit:
            user.save()
        return user

class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')