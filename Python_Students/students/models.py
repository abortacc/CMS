from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    debts = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def attendance_percentage(self):
        student_courses = StudentCourse.objects.filter(student=self)
        total_hours = sum(sc.course.hours for sc in student_courses)
        attended_hours = sum(sc.attended_hours for sc in student_courses)
        if total_hours > 0:
            return (attended_hours / total_hours) * 100
        return 0.0


class Group(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='groups')

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()

    def group_attendance_percentage(self):
        total_percentage = sum(student.attendance_percentage() for student in self.students.all())
        if self.student_count() > 0:
            return total_percentage / self.student_count()
        return 0.0
    

class Subject(models.Model):
    name = models.CharField(max_length=100)
    hours = models.PositiveIntegerField()
    grade = models.FloatField()
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=256)
    time = models.TimeField()

    def __str__(self):
        return f"{self.subject.name} - {self.day} - {self.time}"
    

class Course(models.Model):
    name = models.CharField(max_length=100)
    hours = models.PositiveIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    

class StudentCourse(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(null=True, blank=True)
    attended_hours = models.PositiveIntegerField(default=0)
    has_debt = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade}"

    def attendance_percentage(self):
        if self.course.hours > 0:
            return (self.attended_hours / self.course.hours) * 100
        return 0.0


class Debt(models.Model):
    DEBT_TYPE_CHOICES = [
        ('financial', 'Financial'),
        ('academic', 'Academic'),
    ]

    student_course = models.ForeignKey('StudentCourse', on_delete=models.CASCADE)
    debt_type = models.CharField(max_length=10, choices=DEBT_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    count = models.PositiveIntegerField(blank=True, null=True) 

    def __str__(self):
        return f"{self.get_debt_type_display()} Debt for {self.student_course}"
    


