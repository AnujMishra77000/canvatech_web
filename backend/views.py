from django.shortcuts import render, redirect
from .models import Consultation
import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY

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
            resend.Emails.send({
                "from": settings.RESEND_FROM_EMAIL,
                "to": ["canvatech.info@gmail.com"],
                "subject": "New Consultation Request",
                "html": f"""
<p><b>Name:</b> {consultation.full_name}</p>
<p><b>Company:</b> {consultation.company}</p>
<p><b>Email:</b> {consultation.email}</p>
<p><b>Phone:</b> {consultation.contact_number}</p>
<p><b>Business Details:</b><br>{consultation.business_details}</p>
"""
            })
        except Exception as e:
            print("Admin email failed:", e)

        # 📩 USER WELCOME MAIL
        try:
            resend.Emails.send({
                "from": settings.RESEND_FROM_EMAIL,
                "to": [consultation.email],
                "subject": "Thanks for contacting Canvatech",
                "html": f"""
<p>Hi {consultation.full_name},</p>
<p>Thank you for reaching out!</p>
<p>We’ve received your consultation request and will contact you within 24 hours.</p>
<p>Regards,<br>Canvatech Team</p>
"""
            })
        except Exception as e:
            print("User email failed:", e)

        return redirect("/?success=1")

    return render(request, "index.html", {"success": request.GET.get("success")})
