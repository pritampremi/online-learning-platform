from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.forms import *
from courses.models import *
from django.contrib import messages
from .models import Lesson,LessonProgress
from django.utils import timezone

@login_required
def create_course_view(request):
    if not request.user.is_instructor:
        return redirect('home')  # only instructors can access

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('courses:my_courses')
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def my_courses_view(request):
    if not request.user.is_instructor:
        return redirect('home')
    
    courses = request.user.courses.all()
    return render(request, 'courses/my_courses.html', {'courses': courses})

@login_required
def add_module_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = ModuleForm()

    return render(request, 'courses/add_module.html', {'form': form, 'course': course})


@login_required
def add_lesson_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect('courses:course_detail', course_id=module.course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/add_lesson.html', {'form': form, 'module': module})


@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.prefetch_related('lessons').all()
    quizzes = course.quizzes.all()
    is_instructor = request.user == course.instructor
    is_student = getattr(request.user, 'is_student', False)

    is_enrolled = False
    progress_percent = 0

    if is_student:
        is_enrolled = course.enrollments.filter(student=request.user).exists()

        if is_enrolled:
            total_lessons = sum(module.lessons.count() for module in modules)
            completed_lessons = LessonProgress.objects.filter(
                student=request.user,
                lesson__module__course=course
            ).count()

            if total_lessons > 0:
                progress_percent = int((completed_lessons / total_lessons) * 100)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'quizzes': quizzes,
        'is_instructor': is_instructor,
        'is_student': is_student,
        'is_enrolled': is_enrolled,
        'progress_percent': progress_percent,
    })

from .models import Course
from .forms import CourseForm

@login_required
def edit_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ensure only the instructor can edit
    if request.user != course.instructor:
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:my_courses')
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})


@login_required
def edit_module_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)

    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('courses:course_detail', course_id=module.course.id)
    else:
        form = ModuleForm(instance=module)

    return render(request, 'courses/edit_module.html', {'form': form, 'module': module})


@login_required
def edit_lesson_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('courses:course_detail', course_id=lesson.module.course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'courses/edit_lesson.html', {'form': form, 'lesson': lesson})


@login_required
def delete_module_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    course_id = module.course.id

    if request.method == 'POST':
        module.delete()
        messages.success(request, "Module deleted.")
        return redirect('courses:course_detail', course_id=course_id)

    return render(request, 'courses/confirm_delete.html', {
        'object': module,
        'type': 'Module',
        'cancel_url': 'courses:course_detail',
        'cancel_args': [course_id]
    })


@login_required
def delete_lesson_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    course_id = lesson.module.course.id

    if request.method == 'POST':
        lesson.delete()
        messages.success(request, "Lesson deleted.")
        return redirect('courses:course_detail', course_id=course_id)

    return render(request, 'courses/confirm_delete.html', {
        'object': lesson,
        'type': 'Lesson',
        'cancel_url': 'courses:course_detail',
        'cancel_args': [course_id]
    })


@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not request.user.is_student:
        messages.error(request, "Only students can enroll.")
        return redirect('home')

    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"You are now enrolled in {course.title}")
    return redirect('courses:course_detail', course_id=course.id)

@login_required
def browse_courses_view(request):
    courses = Course.objects.all()
    return render(request, 'courses/browse_courses.html', {'courses': courses})


@login_required
def my_learning_view(request):
    if not request.user.is_student:
        return redirect('home')

    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'courses/my_learning.html', {
        'enrollments': enrollments
    })


@login_required
def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course

    is_instructor = request.user == course.instructor
    is_student = getattr(request.user, 'is_student', False)

    is_enrolled = False
    is_completed = False

    if is_student:
        is_enrolled = course.enrollments.filter(student=request.user).exists()
        if is_enrolled:
            is_completed = LessonProgress.objects.filter(
                student=request.user,
                lesson=lesson
            ).exists()

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'course': course,
        'is_student': is_student,
        'is_instructor': is_instructor,
        'is_enrolled': is_enrolled,
        'is_completed': is_completed,  
    })



@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course

    if request.user.is_student:
        is_enrolled = course.enrollments.filter(student=request.user).exists()
        if is_enrolled:
            LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)

    return redirect('courses:lesson_detail', lesson_id=lesson.id)


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

@login_required
def download_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ensure user is a student and enrolled
    if not getattr(request.user, 'is_student', False):
        return redirect('home')

    enrolled = course.enrollments.filter(student=request.user).exists()
    if not enrolled:
        return redirect('home')

    # Ensure course is fully completed
    total_lessons = course.modules.aggregate(total=models.Count('lessons'))['total']
    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course
    ).count()

    if total_lessons == 0 or completed_lessons < total_lessons:
        return redirect('courses:course_detail', course_id=course.id)

    # Render certificate HTML
    html_string = render_to_string('courses/certificate_template.html', {
        'student': request.user,
        'course': course,
    })

    # Create PDF
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Create response
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{course.title}_certificate.pdf"'
    return response


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def checkout_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.is_instructor:
        return redirect('home')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": int(course.price * 100),  # Razorpay needs amount in paisa
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "courses/checkout.html", {
        "course": course,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


@csrf_exempt
@login_required
def verify_payment_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        # Assume payment success for now
        Enrollment.objects.get_or_create(student=request.user, course=course)
        messages.success(request, "Payment successful! You are now enrolled.")
        return redirect('courses:my_learning')  # or course detail
    return redirect('home')


@login_required
def create_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            return redirect('courses:add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'courses/quiz/create_quiz.html', {'form': form, 'course': course})

@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST, queryset=Option.objects.none())  # FIXED

        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            options = option_formset.save(commit=False)
            for option in options:
                option.question = question
                option.save()

            return redirect('courses:add_question', quiz_id=quiz.id)

    else:
        question_form = QuestionForm()
        option_formset = OptionFormSet(queryset=Option.objects.none())  # FIXED

    return render(request, 'courses/quiz/add_question.html', {
        'quiz': quiz,
        'question_form': question_form,
        'option_formset': option_formset,
    })



@login_required
def attempt_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('options')

    if request.method == 'POST':
        # Create a new attempt each time
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            student=request.user,
            attempted_at=timezone.now()
        )

        score = 0
        total = questions.count()

        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                
                StudentAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=selected_option,
                    student=request.user  # Make sure this is accepted in your model
                )

                if selected_option.is_correct:
                    score += 1

        attempt.score = score
        attempt.save()

        return redirect('courses:view_result', attempt_id=attempt.id)  # Pass attempt_id now

    return render(request, 'courses/quiz/attempt_quiz.html', {
        'quiz': quiz,
        'questions': questions,
    })

@login_required
def view_result_view(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    quiz = attempt.quiz

    # Fetch only answers related to this specific attempt
    answers = StudentAnswer.objects.filter(attempt=attempt)

    return render(request, 'courses/quiz/view_result.html', {
        'quiz': quiz,
        'attempt': attempt,
        'answers': answers,
    })

@login_required
def instructor_quizzes_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    quizzes = course.quizzes.all()

    return render(request, 'courses/quiz/instructor_quizzes.html', {
        'course': course,
        'quizzes': quizzes
    })


@login_required
def quiz_attempts_list_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    attempts = QuizAttempt.objects.filter(quiz=quiz).select_related('student')

    return render(request, 'courses/quiz/quiz_attempts_list.html', {
        'quiz': quiz,
        'attempts': attempts,
    })