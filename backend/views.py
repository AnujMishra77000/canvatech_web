import logging
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Consultation

logger = logging.getLogger(__name__)

def consultation_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")

        if not full_name or not email:
            return redirect("/")

        consultation = Consultation.objects.create(
            full_name=full_name,
            company=request.POST.get("company"),
            email=email,
            contact_number=request.POST.get("contact_number"),
            business_details=request.POST.get("business_details"),
        )

        # 📩 ADMIN MAIL
        try:
            send_mail(
                "New Consultation Request",
                f"""
Name: {consultation.full_name}
Company: {consultation.company}
Email: {consultation.email}
Phone: {consultation.contact_number}

Business Details:
{consultation.business_details}
                """,
                settings.DEFAULT_FROM_EMAIL,
                ["canvatech.info@gmail.com"],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Admin email failed: {e}")

        # 📩 USER MAIL
        try:
            send_mail(
                "Thanks for contacting Canvatech",
                f"""
Hi {consultation.full_name},

Thank you for reaching out!

We’ve received your consultation request and will contact you within 24 hours.

Regards,
Canvatech Team
                """,
                settings.DEFAULT_FROM_EMAIL,
                [consultation.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"User email failed: {e}")

        return redirect("/?success=1")

    return render(request, "index.html", {"success": request.GET.get("success")})
