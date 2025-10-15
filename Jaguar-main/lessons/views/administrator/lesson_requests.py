from django.shortcuts import render
from django.urls import reverse

from lessons.forms.administrator import LessonRequestsFilterForm
from lessons.models import LessonRequest

# Create lesson requests and generated the list of requests
def lesson_requests(request):
    # Get form
    if request.method == "POST":
        form = LessonRequestsFilterForm(request.POST)
    else:
        form = LessonRequestsFilterForm()

    lesson_requests = LessonRequest.objects.all()

    selected_student = form["student_filter"].value()
    selected_term = form["term_filter"].value()
    selected_status = form["status_filter"].value()

    if selected_student not in [None, ""]:
        lesson_requests = lesson_requests.filter(user=selected_student)

    if selected_status not in [None, "", "all"]:
        if selected_status == "fulfilled":
            lesson_requests = lesson_requests.filter(is_fulfilled=True)
        else:
            lesson_requests = lesson_requests.filter(is_fulfilled=False)
    
    # Convert lesson request to a card
    def convert_lesson_request_to_card(lesson_request):
        heading = lesson_request.user
        no_of_lessons = str(lesson_request.no_of_lessons)
        lesson_duration = f"{lesson_request.lesson_duration_in_mins} minutes"
        lesson_interval = f"{lesson_request.lesson_interval_in_days} days"

        book_url = reverse('administrator/lesson-requests/book', kwargs={"lesson_request_id": lesson_request.pk})
        view_url = reverse('administrator/lesson-requests/view', kwargs={"lesson_request_id": lesson_request.pk})
        edit_url = reverse('administrator/lesson-requests/edit', kwargs={"pk": lesson_request.pk})
        delete_url = reverse('administrator/lesson-requests/delete', kwargs={"pk": lesson_request.pk})
        
        # description of the information
        return {
            "heading":
                heading,
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
            "buttons": [{
                "name": "View",
                "url": view_url,
                "type": "outline-primary",
            }, {
                "name": "Book",
                "url": book_url,
                "type": "outline-primary",
            }, {
                "name": "Edit",
                "url": edit_url,
                "type": "outline-primary",
            }, {
                "name": "Delete",
                "url": delete_url,
                "type": "outline-danger",
            }],
        }

    cards = map(convert_lesson_request_to_card, lesson_requests)

    # Return page
    return render(
        request, "administrator/lesson_requests.html", {
            "allowed_roles": ["Administrator", "Director"],
            "lesson_requests": lesson_requests,
            "form": form,
            "dashboard": {
                "heading": "Lesson Requests",
                "subheading": "Fulfill and delete student lesson requests."
            },
            "cards": cards
        })
