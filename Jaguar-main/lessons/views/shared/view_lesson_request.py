from django.shortcuts import render

from lessons.models import LessonRequest


def view_lesson_request(request, lesson_request_id):
    go_back_url = f"{request.user.role.lower()}/lesson-requests"

    return render(
        request, "shared/view_lesson_request.html", {
            "allowed_roles": ["Student", "Administrator", "Director"],
            "dashboard": {
                "heading": f"View Lesson Request #{lesson_request_id}",
                "subheading": "See more details about this lesson request."
            },
            "lesson_request": LessonRequest.objects.get(pk=lesson_request_id),
            "go_back_url": go_back_url,
        })