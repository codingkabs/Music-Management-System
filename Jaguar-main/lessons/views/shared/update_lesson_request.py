from django.views.generic.edit import UpdateView

from lessons.forms.shared import LessonRequestEditForm
from lessons.models import LessonRequest


class LessonRequestUpdateView(UpdateView):
    model = LessonRequest
    form_class = LessonRequestEditForm
    template_name = "edit.html"
    extra_context = {
        "allowed_roles": ["Student", "Administrator", "Director"],
        "dashboard": {
            "heading": "Modify lesson request",
            "subheading": "Change details about this lesson request."
        }
    }

    def get_success_url(self):
        return f"/{self.request.user.role.lower()}/lesson-requests"