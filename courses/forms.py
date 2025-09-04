from django import forms
from courses.models import *
from django.forms import modelformset_factory

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'price', 'thumbnail']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'order']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'content', 'pdf', 'order']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

OptionFormSet = modelformset_factory(Option, fields=('text', 'is_correct'), extra=4, can_delete=False)