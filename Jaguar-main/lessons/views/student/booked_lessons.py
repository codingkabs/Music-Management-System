from django.shortcuts import render

from lessons.helpers import get_lesson_price
from lessons.models import Lesson, LessonRequest


def booked_lessons(request):
    # Get all lesson requests for this user
    lesson_requests = LessonRequest.objects.filter(user=request.user, is_fulfilled=True)

    # Get lessons with lesson requests belonging to the user
    lessons = Lesson.objects.none()

    for lesson_request in lesson_requests:
        lessons = lessons | Lesson.objects.filter(lesson_request=lesson_request)

    # Convert lessons to cards
    cards = []

    for lesson in lessons:
        heading = lesson.datetime.strftime("%d %B %Y (%H:%M)")

        cards.append({
            "heading":
                heading,
            "info": [{
                "title": "Price",
                "description": get_lesson_price(lesson),
            }, {
                "title": "Teacher",
                "description": lesson.teacher,
            }, {
                "title": "Duration",
                "description": f"{lesson.duration} minutes",
            }, {
                "title": "Further Information",
                "description": lesson.further_information,
            }]
        })

    return render(
        request, "student/booked_lessons.html", {
            "allowed_roles": ["Student"],
            "dashboard": {
                "heading": "Booked Lessons",
                "subheading": "View all your booked lessons."
            },
            "cards": cards,
        })
