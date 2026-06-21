import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

def index(request):
    return render(request, 'portfolio/index.html')

@csrf_exempt
def contact(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        data    = json.loads(request.body)
        name    = data.get('name', '').strip()
        email   = data.get('email', '').strip()
        phone   = data.get('phone', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return JsonResponse({'success': False, 'error': 'Name, email and message are required.'}, status=400)

        # Save to PostgreSQL
        ContactMessage.objects.create(
            name=name, email=email, phone=phone,
            subject=subject, message=message
        )

        # ── Confirmation email to sender ──────────────────────────────────────
        confirmation_html = f"""
        <div style="font-family:Arial,sans-serif;max-width:620px;margin:auto;background:#06060f;color:#e0e0e0;border-radius:16px;overflow:hidden;border:1px solid #1a3a6b;">
          <div style="background:linear-gradient(135deg,#0d1b4b 0%,#1a3a6b 50%,#0d6efd 100%);padding:36px;text-align:center;">
            <h1 style="color:#fff;margin:0;font-size:28px;letter-spacing:2px;">LAXMINARAYAN PATEL</h1>
            <p style="color:#7ab3ff;margin:8px 0 0;font-size:14px;letter-spacing:3px;">SR. MANAGER ACCOUNTS</p>
          </div>
          <div style="padding:32px;">
            <h2 style="color:#4da6ff;border-bottom:1px solid #1a3a6b;padding-bottom:12px;">✅ Message Received</h2>
            <p style="color:#ccc;">Dear <strong style="color:#fff;">{name}</strong>,</p>
            <p style="color:#aaa;line-height:1.7;">Thank you for getting in touch! I have received your message and will respond as soon as possible. Here's a copy of what you submitted:</p>
            <table style="width:100%;border-collapse:collapse;margin:24px 0;background:#0d0d1f;border-radius:8px;overflow:hidden;">
              <tr><td style="padding:12px 16px;color:#888;width:120px;">Name</td><td style="padding:12px 16px;color:#fff;border-left:1px solid #1a3a6b;">{name}</td></tr>
              <tr style="background:#06060f;"><td style="padding:12px 16px;color:#888;">Email</td><td style="padding:12px 16px;color:#fff;border-left:1px solid #1a3a6b;">{email}</td></tr>
              <tr><td style="padding:12px 16px;color:#888;">Phone</td><td style="padding:12px 16px;color:#fff;border-left:1px solid #1a3a6b;">{phone or '—'}</td></tr>
              <tr style="background:#06060f;"><td style="padding:12px 16px;color:#888;">Subject</td><td style="padding:12px 16px;color:#fff;border-left:1px solid #1a3a6b;">{subject or '—'}</td></tr>
              <tr><td style="padding:12px 16px;color:#888;vertical-align:top;">Message</td><td style="padding:12px 16px;color:#fff;border-left:1px solid #1a3a6b;line-height:1.6;">{message}</td></tr>
            </table>
            <p style="color:#aaa;">I look forward to connecting with you.</p>
            <p style="color:#7ab3ff;margin-top:24px;">Warm regards,<br><strong style="color:#fff;">Laxminarayan Patel</strong><br>
            <span style="color:#888;font-size:13px;">Sr. Manager Accounts | WTC (Nagpur) Pvt. Ltd.<br>📞 +91-9425027682 | 📧 laxmihardi191@gmail.com</span></p>
          </div>
          <div style="background:#0d0d1f;padding:16px;text-align:center;color:#555;font-size:12px;border-top:1px solid #1a3a6b;">
            WTC (Nagpur) Pvt. Ltd., Sitabuldi, Nagpur, Maharashtra — 440012
          </div>
        </div>
        """
        try:
            send_mail(
                subject=f"Thank you for contacting me — {subject or 'Your Message'}",
                message=f"Dear {name},\nThank you for reaching out. I'll get back to you soon.\n\n— Laxminarayan Patel",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=confirmation_html,
                fail_silently=True,   # ← THIS WAS FALSE BEFORE 22-06-2026
            )
            # Notify yourself
            # Notify yourself
            notify_html = f"""
            <div style="font-family:Arial,sans-serif;max-width:620px;margin:auto;background:#06060f;color:#e0e0e0;border-radius:16px;overflow:hidden;border:1px solid #1a3a6b;">
            <div style="background:linear-gradient(135deg,#0d1b4b 0%,#1a3a6b 50%,#0d6efd 100%);padding:28px 36px;display:flex;align-items:center;justify-content:space-between;">
                <div>
                <h1 style="color:#fff;margin:0;font-size:22px;letter-spacing:1px;">📬 New Contact Received</h1>
                <p style="color:#7ab3ff;margin:6px 0 0;font-size:13px;">Someone filled your portfolio contact form</p>
                </div>
                <div style="background:rgba(255,255,255,.1);padding:10px 18px;border-radius:8px;text-align:center;">
                <div style="color:#fff;font-size:22px;font-weight:700;">!</div>
                <div style="color:#7ab3ff;font-size:10px;letter-spacing:1px;">ACTION</div>
                </div>
            </div>
            <div style="padding:32px;">
                <table style="width:100%;border-collapse:collapse;border-radius:8px;overflow:hidden;">
                <tr style="background:#0d0d1f;">
                    <td style="padding:14px 18px;color:#7ab3ff;font-size:12px;font-weight:700;letter-spacing:1px;width:120px;border-bottom:1px solid #1a3a6b;">👤 NAME</td>
                    <td style="padding:14px 18px;color:#fff;font-size:15px;font-weight:600;border-bottom:1px solid #1a3a6b;">{name}</td>
                </tr>
                <tr style="background:#06060f;">
                    <td style="padding:14px 18px;color:#7ab3ff;font-size:12px;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1a3a6b;">📧 EMAIL</td>
                    <td style="padding:14px 18px;border-bottom:1px solid #1a3a6b;"><a href="mailto:{email}" style="color:#4da6ff;font-size:15px;">{email}</a></td>
                </tr>
                <tr style="background:#0d0d1f;">
                    <td style="padding:14px 18px;color:#7ab3ff;font-size:12px;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1a3a6b;">📞 PHONE</td>
                    <td style="padding:14px 18px;color:#fff;font-size:15px;border-bottom:1px solid #1a3a6b;"><a href="tel:{phone}" style="color:#4da6ff;">{phone or '—'}</a></td>
                </tr>
                <tr style="background:#06060f;">
                    <td style="padding:14px 18px;color:#7ab3ff;font-size:12px;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1a3a6b;">📌 SUBJECT</td>
                    <td style="padding:14px 18px;color:#fff;font-size:15px;border-bottom:1px solid #1a3a6b;">{subject or '—'}</td>
                </tr>
                <tr style="background:#0d0d1f;">
                    <td style="padding:14px 18px;color:#7ab3ff;font-size:12px;font-weight:700;letter-spacing:1px;vertical-align:top;">💬 MESSAGE</td>
                    <td style="padding:14px 18px;color:#e0e0e0;font-size:14px;line-height:1.8;">{message}</td>
                </tr>
                </table>
                <div style="margin-top:24px;padding:16px 20px;background:rgba(45,107,228,.1);border:1px solid rgba(45,107,228,.3);border-radius:8px;">
                <p style="margin:0;color:#7ab3ff;font-size:13px;">⚡ Reply directly to this email or click the email above to respond to {name}.</p>
                </div>
            </div>
            <div style="background:#0d0d1f;padding:16px;text-align:center;color:#555;font-size:12px;border-top:1px solid #1a3a6b;">
                Laxminarayan Patel Portfolio — WTC (Nagpur) Pvt. Ltd., Sitabuldi, Nagpur
            </div>
            </div>
            """
            send_mail(
                subject=f"📬 New Contact from {name} — {subject or 'Portfolio Enquiry'}",
                message=f"New contact from {name} | {email} | {phone}\n\nMessage: {message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                html_message=notify_html,
                fail_silently=True,
            )
            email_sent = True
        except Exception as e:
            print(f"Email error: {e}")
            email_sent = False

        return JsonResponse({'success': True, 'email_sent': email_sent})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
