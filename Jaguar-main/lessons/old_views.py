from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from lessons.forms import (LessonCreateForm, LessonEditForm, LessonRequestForm, LogInForm, SignUpForm,
                           AdministratorCreationForm)
from lessons.helpers import get_lesson_price
from lessons.models import Invoice, Lesson, LessonRequest

# Create your views here.
"""
Main 'site' pages (index page, log in, sign up and log out).
"""


def home(request):
    return render(request, "home.html", {"allowed_roles": ["Anonymous"]})


def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                # Redirect user to appropriate user dashboard
                if (user.role == "Student"):
                    return redirect("student")
                elif (user.role == "Administrator"):
                    return redirect("administrator")
                elif (user.role == "Director"):
                    return redirect("director")

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")

    form = LogInForm()

    return render(request, "log_in.html", {"form": form, "allowed_roles": ["Anonymous"]})


def log_out(request):
    logout(request)

    return redirect("home")


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            # Redirect user to appropriate user dashboard
            if (user.role == "Student"):
                return redirect("student")
            elif (user.role == "Administrator"):
                return redirect("administrator")
            elif (user.role == "Director"):
                return redirect("director")
    else:
        form = SignUpForm()

    return render(request, "sign_up.html", {"form": form, "allowed_roles": ["Anonymous"]})


"""
User dashboards for each type of user (student, administrator and director).
"""


def student(request):
    return redirect("student/lesson-requests")


def administrator(request):
    return redirect("administrator/lesson-requests")


def director(request):
    return redirect("administrator/lesson-requests")


"""
Subpages for students.
"""


def student_lesson_requests(request):
    if request.user.is_authenticated:
        if (LessonRequest.objects.filter(user_id=request.user.id).exists()):
            lesson = LessonRequest.objects.get(user_id=request.user.id)
            return render(request, "manage_lesson_requests.html", {'allowed_roles': ["Student"], "lesson": lesson})
    return render(request, "manage_lesson_requests.html", {'allowed_roles': ['Student']})


def student_delete_lesson_requests(request, id):
    lesson = LessonRequest.objects.get(id=id)
    if request.user.is_authenticated:
        if lesson.user_id == request.user.id:
            lesson.delete()
        return redirect("student/lesson_requests")
    else:
        return redirect("student/lesson_requests")


def student_edit_lesson_requests(request, id):
    lesson_request = LessonRequest.objects.get(id=id)
    if request.user.is_authenticated:
        form = LessonRequestForm(current_user=request.user, instance=lesson_request)
        if request.method == 'POST':
            form = LessonRequestForm(request.POST, instance=lesson_request)
            if form.is_valid():
                form.save()
                return redirect("student/lesson_requests")
        lesson_request.delete()
    return render(request, "lesson_request.html", {"form": form, "allowed_roles": ["Student"]})


def student_manage_dependents(request):
    return HttpResponse("Page does not exist yet.")


def student_transactions(request):
    return HttpResponse("Page does not exist yet.")


"""
Subpages for administrators.
"""


def administrator_lesson_requests_book(request, lesson_request_id):
    lesson_request = LessonRequest.objects.get(pk=lesson_request_id)

    # Get lessons for this lesson request (if they exist)
    lessons = Lesson.objects.filter(lesson_request=lesson_request)

    # Convert lessons to cards
    cards = []

    for lesson in lessons:
        edit_url = reverse("administrator/lesson-requests/book/lessons/edit",
                           kwargs={
                               "lesson_request_id": lesson_request.pk,
                               "pk": lesson.pk
                           })
        delete_url = reverse("administrator/lesson-requests/book/lessons/delete",
                             kwargs={
                                 "lesson_request_id": lesson_request.pk,
                                 "pk": lesson.pk
                             })

        heading = lesson.datetime.strftime("%d %B %Y (%H:%M)")

        cards.append({
            "heading":
                heading,
            "info": [{
                "title": "Teacher",
                "description": lesson.teacher,
            }, {
                "title": "Duration",
                "description": f"{lesson.duration} minutes",
            }, {
                "title": "Further Information",
                "description": lesson.further_information,
            }, {
                "title": "Price",
                "description": get_lesson_price(lesson),
            }],
            "buttons": [{
                "name": "Edit",
                "url": edit_url,
                "type": "outline-primary"
            }, {
                "name": "Delete",
                "url": delete_url,
                "type": "outline-danger",
            }]
        })

    return render(
        request, "administrator/lesson_requests/book.html", {
            "allowed_roles": ["Administrator", "Director"],
            "dashboard": {
                "heading": f"Book Lessons for Lesson Request #{lesson_request_id}",
                "subheading": "Book lessons for this lesson request."
            },
            "lesson_request": lesson_request,
            "cards": cards,
        })


def administrator_lesson_requests_book_finalise_booking(request, lesson_request_id):
    lesson_request = LessonRequest.objects.get(pk=lesson_request_id)
    lesson_request.is_fulfilled = True
    lesson_request.save()

    invoice = Invoice.objects.create(lesson_request=lesson_request, user=lesson_request.user)
    invoice.save()

    return redirect(f"/administrator/lesson-requests")


def administrator_lesson_requests_book_lessons_delete(request, lesson_request_id, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.delete()

    return redirect(f"/administrator/lesson-requests/book/{lesson_request_id}")


def administrator_lesson_requests_delete(request, lesson_request_id):
    lesson_request = LessonRequest.objects.get(pk=lesson_request_id)
    lesson_request.delete()

    return redirect("administrator/lesson-requests")


"""
Subpages for directors.
"""


def director_lesson_requests(request):
    return render(
        request, "administrator/lesson_requests.html", {
            "allowed_roles": ["Administrator", "Director"],
            "dashboard": {
                "heading": "Lesson Requests",
                "subheading": "View student lesson requests."
            }
        })


def director_student_balances(request):
    return HttpResponse("Page does not exist yet.")


def director_manage_administrators(request):
    return render(
        request, "director/manage_administrators.html", {
            "allowed_roles": ["Director"],
            "dashboard": {
                "heading": "Administrator Accounts",
                "subheading": "View and manage administrator accounts"
            }
        })


def director_create_administrator(request):
    if request.method == "POST":
        form = AdministratorCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            return redirect("director")

    else:
        form = AdministratorCreationForm()

    return render(request, "director/manage_administrator/create_administrator.html", {
        "form": form,
        "allowed_roles": ["Director"]
    })


""" Views for deleting objects. """


class AdministratorLessonDeleteView(DeleteView):
    model = Lesson
    template_name = "delete.html"
    extra_context = {
        "allowed_roles": ["Administrator", "Director"],
        "dashboard": {
            "heading": "Delete lesson",
            "subheading": "Confirm deletion of lesson."
        }
    }

    def get_success_url(self):
        return f"/administrator/lesson-requests/book/{self.object.lesson_request.pk}"


class AdministratorLessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonEditForm
    template_name = "edit.html"
    extra_context = {
        "allowed_roles": ["Administrator", "Director"],
        "dashboard": {
            "heading": "Modify lesson",
            "subheading": "Change details about this lesson."
        }
    }

    def get_success_url(self):
        return f"/administrator/lesson-requests/book/{self.object.lesson_request.pk}"


class AdministratorLessonCreateView(CreateView):
    model = Lesson
    form_class = LessonCreateForm
    template_name = "edit.html"
    extra_context = {
        "allowed_roles": ["Administrator", "Director"],
        "dashboard": {
            "heading": "Create new lesson",
            "subheading": "Create a new lesson by specifying details."
        }
    }

    def get_success_url(self):
        return f"/administrator/lesson-requests/book/{self.object.lesson_request.pk}"

    def get_initial(self):
        initial = super(AdministratorLessonCreateView, self).get_initial()

        lesson_request = LessonRequest.objects.filter(pk=self.kwargs["lesson_request_id"]).first()

        initial["lesson_request"] = lesson_request.pk
        initial["user"] = lesson_request.user.pk
        return initial
