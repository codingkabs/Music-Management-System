from django.shortcuts import render, redirect

from lessons.forms import LessonRequestForm


def lesson_request(request):
    if request.method == "POST":
        form = LessonRequestForm(request.POST, current_user=request.user)

        if form.is_valid():
            form.save()

            return redirect("student")
    else:
        form = LessonRequestForm(current_user=request.user)

    return render(
        request, "lesson_request.html", {
            "form": form,
            "allowed_roles": ["Student"],
            "dashboard": {
                "heading": "Make Lesson Request",
                "subheading": "Submit requests for sets of lessons."
            }
        })
