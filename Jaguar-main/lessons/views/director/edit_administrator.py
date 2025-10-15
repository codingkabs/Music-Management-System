from django.views.generic.edit import UpdateView

from lessons.models import User
from lessons.forms.director import AdminEditForm


class AdminUpdateView(UpdateView):
    model = User
    form_class = AdminEditForm
    template_name = "edit.html"
    extra_context = {
        "allowed_roles": ["Administrator", "Director"],
        "dashboard": {
            "heading": "Modify this administrator account",
            "subheading": "Change details about this administrator account."
        }
    }

    def get_success_url(self):
        return f"/director/manage-administrators"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context