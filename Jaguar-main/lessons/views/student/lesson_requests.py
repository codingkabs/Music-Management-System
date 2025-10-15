from django.shortcuts import render
from django.urls import reverse

from lessons.forms.student import LessonRequestsFilterForm
from lessons.models import LessonRequest


def lesson_requests(request):
    # Get form
    if request.method == "POST":
        form = LessonRequestsFilterForm(request.POST)
    else:
        form = LessonRequestsFilterForm()

    # Generate correct list of requests to show
    lesson_requests = LessonRequest.objects.all()

    selected_term = form["term_filter"].value()
    selected_status = form["status_filter"].value()

    lesson_requests = lesson_requests.filter(user=request.user)

    if selected_status not in [None, "", "all"]:
        if selected_status == "fulfilled":
            lesson_requests = lesson_requests.filter(is_fulfilled=True)
        else:
            lesson_requests = lesson_requests.filter(is_fulfilled=False)

    def convert_lesson_request_to_card(lesson_request):
        heading = lesson_request.user
        no_of_lessons = str(lesson_request.no_of_lessons)
        lesson_duration = f"{lesson_request.lesson_duration_in_mins} minutes"
        lesson_interval = f"{lesson_request.lesson_interval_in_days} days"

        view_url = reverse('student/lesson-requests/view', kwargs={"lesson_request_id": lesson_request.pk})
        lessons_url = reverse('student/lesson-requests/view-lessons', kwargs={"lesson_request_id": lesson_request.pk})
        edit_url = reverse('student/lesson-requests/edit', kwargs={"pk": lesson_request.pk})
        delete_url = reverse('student/lesson-requests/delete', kwargs={"pk": lesson_request.pk})

        buttons = [{
            "name": "View",
            "url": view_url,
            "type": "outline-primary",
        }]

        if lesson_request.is_fulfilled:
            buttons.append({"name": "Lessons", "url": lessons_url, "type": "outline-primary"})
        else:
            buttons.append({
                "name": "Edit",
                "url": edit_url,
                "type": "outline-primary",
            })
            buttons.append({
                "name": "Delete",
                "url": delete_url,
                "type": "outline-danger",
            })

        return {
            "heading": heading,
            "info": [{
                "title": "Number of Lessons",
                "description": no_of_lessons,
            }, {
                "title": "Lesson Duration",
                "description": lesson_duration,
            }, {
                "title": "Interval Between Lessons",
                "description": lesson_interval,
            }],
            "buttons": buttons,
        }

    cards = map(convert_lesson_request_to_card, lesson_requests)

    # Return page
    return render(
        request, "student/lesson_requests.html", {
            "allowed_roles": ["Student"],
            "lesson_requests": lesson_requests,
            "form": form,
            "dashboard": {
                "heading": "Lesson Requests",
                "subheading": "Fulfill and delete your lesson requests."
            },
            "cards": cards
        })
