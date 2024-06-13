from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Student, Subject, Schedule, Course, StudentCourse, Debt
from .forms import StudentForm, GroupForm, SubjectForm, ScheduleForm, BatchSubjectForm, CourseForm, GradeForm, AddExistingCourseForm, StudentCourseForm
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

# Create your views here.
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'students/group_list.html', {'groups': groups})


def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    students = group.students.all()
    return render(request, 'students/group_detail.html', {'group': group, 'students': students})


def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'students/group_form.html', {'form': form})


def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'students/group_confirm_delete.html', {'group': group})
    

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            group = form.cleaned_data['group']
            group.students.add(student)
            return redirect('group_detail', pk=group.pk)
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})


@csrf_exempt
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_courses = StudentCourse.objects.filter(student=student)
    
    total_attended_hours = sum(course.attended_hours for course in student_courses)
    total_hours = sum(course.course.hours for course in student_courses)
    
    if total_hours > 0:
        total_attendance_percentage = (total_attended_hours / total_hours) * 100
    else:
        total_attendance_percentage = 0.0
    
    total_grades = sum(course.grade for course in student_courses if course.grade is not None)
    num_grades = sum(1 for course in student_courses if course.grade is not None)
    
    average_grade = total_grades / num_grades if num_grades > 0 else 0.0
    
    total_debts = Debt.objects.filter(student_course__in=student_courses).count()
    
    financial_debt = Decimal(request.session.get(f'financial_debt_{student.pk}', '0.0'))
    
    if request.method == 'POST':
        if 'financial_debt' in request.POST:
            financial_debt = Decimal(request.POST['financial_debt'])
            request.session[f'financial_debt_{student.pk}'] = str(financial_debt)
        return redirect('student_detail', pk=student.pk)
    
    context = {
        'student': student,
        'student_courses': student_courses,
        'total_attended_hours': total_attended_hours,
        'total_hours': total_hours,
        'total_attendance_percentage': total_attendance_percentage,
        'average_grade': average_grade,
        'total_debts': total_debts,
        'financial_debt': financial_debt,
    }
    return render(request, 'students/student_detail.html', context)

def toggle_student_debt(request, pk):
    student_course_pk = request.POST.get('student_course_pk')
    student_course = get_object_or_404(StudentCourse, pk=student_course_pk)
    
    # Check if debt already exists for the student_course
    debt, created = Debt.objects.get_or_create(student_course=student_course, defaults={'debt_type': 'academic'})
    
    if not created:
        # If the debt already exists, delete it
        debt.delete()
    
    return redirect('student_detail', pk=pk)


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('group_list')


def home(request):
    context = {}
    return render(request, 'students/home.html', context)


def add_subject(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.student = student
            subject.save()
            return redirect('student_detail', pk=pk)
    else:
        form = SubjectForm()
    return render(request, 'students/add_subject.html', {'form': form})


def add_schedule(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.subject = subject
            schedule.save()
            return redirect('student_detail', pk=subject.student.pk)
    else:
        form = ScheduleForm()
    return render(request, 'students/add_schedule.html', {'form': form})


def add_batch_subject(request):
    if request.method == 'POST':
        form = BatchSubjectForm(request.POST)
        if form.is_valid():
            subject_data = form.cleaned_data
            students = Student.objects.all()
            for student in students:
                subject_data['student'] = student
                Subject.objects.create(**subject_data)
            return redirect('home')
    else:
        form = BatchSubjectForm()
    return render(request, 'students/add_batch_subject.html', {'form': form})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            for student in course.group.students.all():
                StudentCourse.objects.create(student=student, course=course)
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})


def delete_student_course(request, pk):
    student_course = get_object_or_404(StudentCourse, pk=pk)
    student_id = student_course.student.id
    if request.method == 'POST':
        student_course.delete()
        return redirect('student_detail', pk=student_id)


def edit_grade(request, pk):
    student_course = get_object_or_404(StudentCourse, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=student_course)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student_course.student.pk)
    else:
        form = GradeForm(instance=student_course)
    return render(request, 'students/edit_grade.html', {'form': form, 'student_course': student_course})


def add_existing_course(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = AddExistingCourseForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            StudentCourse.objects.create(student=student, course=course)
            return redirect('student_detail', pk=student_id)
    else:
        form = AddExistingCourseForm()
    return render(request, 'students/add_existing_course.html', {'form': form, 'student': student})


def manage_subjects(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
        if 'subject_submit' in request.POST:
            subject_form = SubjectForm(request.POST)
            if subject_form.is_valid():
                subject_form.save()
                return redirect('manage_subjects')
        elif 'course_submit' in request.POST:
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                return redirect('manage_subjects')
    else:
        subject_form = SubjectForm()
        course_form = CourseForm()

    context = {
        'subjects': subjects,
        'courses': courses,
        'subject_form': subject_form,
        'course_form': course_form,
    }

    return render(request, 'students/manage_subjects.html', context)


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    subject.delete()
    return redirect('manage_subjects')


def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return redirect('manage_subjects')


def edit_student_course(request, pk):
    student_course = get_object_or_404(StudentCourse, pk=pk)
    if request.method == 'POST':
        form = StudentCourseForm(request.POST, instance=student_course)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student_course.student.pk)
    else:
        form = StudentCourseForm(instance=student_course)
    return render(request, 'students/edit_student_course.html', {'form': form, 'student_course': student_course})


def student_debt_list(request):
    selected_group = request.GET.get('group')
    
    students = Student.objects.all()
    if selected_group:
        students = students.filter(groups__id=selected_group)

    debt_students = []

    for student in students:

        student_courses = StudentCourse.objects.filter(student=student)
        total_debts = Debt.objects.filter(student_course__in=student_courses).count()
        attendance_percentage = student.attendance_percentage()
        financial_debt = Decimal(request.session.get(f'financial_debt_{student.pk}', '0.0'))

        # Если есть академические или финансовые долги, добавляем студента в список
        if total_debts > 0 or financial_debt > 0:
            group = student.groups.first()
            debt_students.append({
                'student': student,
                'total_debts': total_debts,
                'attendance_percentage': attendance_percentage,
                'financial_debt': financial_debt,
                'group': student.groups.first()
            })
    
    groups = Group.objects.all()
    
    context = {
        'debt_students': debt_students,
        'groups': groups,
        'selected_group': selected_group,
    }
    
    return render(request, 'students/debt_list.html', context)
