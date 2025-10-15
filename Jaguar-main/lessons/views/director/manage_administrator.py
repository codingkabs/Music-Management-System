from django.shortcuts import render
from django.urls import reverse

from lessons.models import User


def administrator_list(request):

    # Generate correct list of requests to show
    administrators = User.objects.filter(role="Administrator")

    def convert_administrators_to_card(administrator):
        heading = administrator.email
        firstname = administrator.first_name
        lastname = administrator.last_name

        edit_url = reverse('director/manage-administrators/edit', kwargs={"pk": administrator.pk})
        delete_url = reverse('director/manage-administrators/delete', kwargs={"pk": administrator.pk})

        return {
            "heading":
                heading,
            "info": [{
                "title": "First Name",
                "description": firstname,
            }, {
                "title": "Last Name",
                "description": lastname,
            }],
            "buttons": [{
                "name": "Edit",
                "url": edit_url,
                "type": "outline-primary",
            }, {
                "name": "Delete",
                "url": delete_url,
                "type": "outline-danger",
            }],
        }

    cards = map(convert_administrators_to_card, administrators)
    # Return page
    return render(
        request, "director/manage_administrators.html", {
            "allowed_roles": ["Director"],
            "administrators": administrators,
            "dashboard": {
                "heading": "Administrators",
                "subheading": "Manage administrators."
            },
            "cards": cards
        })
