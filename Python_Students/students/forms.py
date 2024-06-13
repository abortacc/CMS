from django import forms
from .models import Student, Group, Subject, Schedule, Course, StudentCourse

class StudentForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'debts', 'group']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'debts': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'hours', 'grade']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'day', 'time']


class BatchSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'hours', 'grade']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'hours', 'group']

    group = forms.ModelChoiceField(queryset=Group.objects.all())


class StudentCourseForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['grade', 'attended_hours']


class GradeForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['grade']


class AddExistingCourseForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Select Course")