from django.shortcuts import render
from django.urls import reverse

from lessons.helpers import get_lesson_price
from lessons.models import Lesson, LessonRequest


def view_lessons(request, lesson_request_id):
    lesson_request = LessonRequest.objects.get(pk=lesson_request_id)

    # Get lessons for this lesson request (if they exist)
    lessons = Lesson.objects.filter(lesson_request=lesson_request)

    # Convert lessons to cards
    cards = []

    for lesson in lessons:
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
            }]
        })

    return render(
        request, "student/view_lessons.html", {
            "allowed_roles": ["Student"],
            "dashboard": {
                "heading": "Booked Lessons",
                "subheading": "View your booked lessons for this lesson request."
            },
            "lesson_request": lesson_request,
            "cards": cards,
        })
