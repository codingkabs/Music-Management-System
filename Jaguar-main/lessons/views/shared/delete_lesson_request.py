from django.views.generic.edit import DeleteView

from lessons.models import LessonRequest


class LessonRequestDeleteView(DeleteView):
    model = LessonRequest
    template_name = "delete.html"
    extra_context = {
        "allowed_roles": ["Student", "Administrator", "Director"],
        "dashboard": {
            "heading": "Delete lesson request",
            "subheading": "Confirm deletion of lesson request."
        }
    }

    def get_success_url(self):
        return f"/{self.request.user.role.lower()}/lesson-requests"