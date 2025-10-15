from django.core.validators import MinValueValidator
from django.db import models

from lessons.models import Invoice, User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    # NOTE: DecimalField is okay because it uses a fixed-point representation.
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])