from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "company",
        "email",
        "contact_number",
        "submitted_at",
    )
    search_fields = (
        "full_name",
        "company",
        "email",
        "contact_number",
    )
    list_filter = ("submitted_at",)
