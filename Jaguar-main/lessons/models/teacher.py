from django.db import models

# Create class Teacher, setting firt and last name.
# max length of 255
class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
