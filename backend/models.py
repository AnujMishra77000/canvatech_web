from django.db import models
from django.core.validators import RegexValidator

class Consultation(models.Model):
    full_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=10,
        validators=[
            RegexValidator(r'^\d{10}$', "Must be exactly 10 digits.")
        ],
        null = True
)
    business_details = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name