import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP Configuration for Gmail
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.getenv("SMTP_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_sales_email(to_email, business_name, pain_point, sender_name="Sani V."):
    """
    Sends a personalized sales email using Gmail SMTP.
    """
    
    # Value Proposition & ROI Analysis
    if pain_point == "low reviews":
        point_text = "I noticed your business online presence has significant room for growth in customer reviews. Our automated Reputation Engine doesn't just manage feedback—it actively converts happy customers into 5-star reviews on autopilot. For most clinics, this increase in social proof directly translates to a 20-30% lift in new patient inquiries within the first 60 days."
    elif pain_point == "missing website":
        point_text = "I couldn't locate a dedicated website for your business. Statistics show that local businesses without a high-converting digital storefront lose nearly 40% of potential bookings to competitors who are easier to find and book online. We provide premium, one-time ownership SaaS websites that function as your 24/7 sales team, generating ROI by capturing every lead that would otherwise have been missed."
    else:
        point_text = f"We specialize in solving operational inefficiencies through 24/7 AI assistance and workflow automation. By automating up to 70% of your routine customer inquiries and internal reporting, we significantly reduce overhead costs while increasing your response speed—a combination that typically results in an immediate positive ROI."

    primary_blue = "#1e3a8a"
    light_blue_bg = "#f0f4ff"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ROI-Driven AI Automation for {business_name}</title>
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a1a1a; background-color: #f4f4f4; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 0; border-radius: 6px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
            .header {{ background-color: {primary_blue}; color: #ffffff; padding: 40px 20px; text-align: center; }}
            .header h1 {{ margin: 0; letter-spacing: 2px; text-transform: uppercase; font-size: 26px; }}
            .body-content {{ padding: 40px; }}
            .service-card {{ background-color: {light_blue_bg}; padding: 22px; margin-bottom: 20px; border-radius: 4px; border-left: 5px solid {primary_blue}; }}
            .service-title {{ font-weight: bold; color: {primary_blue}; display: block; margin-bottom: 6px; font-size: 16px; }}
            .cta {{ text-align: center; margin: 40px 0; }}
            .cta-button {{ background-color: {primary_blue}; color: #ffffff !important; padding: 18px 35px; text-decoration: none; font-weight: bold; display: inline-block; text-transform: uppercase; letter-spacing: 1px; font-size: 14px; border-radius: 4px; }}
            .social-footer {{ background-color: #ffffff; padding: 30px; text-align: center; border-top: 1px solid #eeeeee; }}
            .social-icon {{ display: inline-block; margin: 0 12px; vertical-align: middle; }}
            .social-icon img {{ width: 24px; height: 24px; display: block; }}
            .footer-text {{ font-size: 11px; color: #666666; margin-top: 25px; text-align: center; line-height: 1.5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header"><h1>MoonLIT Arc</h1></div>
            <div class="body-content">
                <p>Dear Team at {business_name},</p>
                <p>I am reaching out from MoonLIT Arc. We help high-growth businesses eliminate manual bottlenecks and maximize revenue potential.</p>
                <p>{point_text}</p>
                <div class="service-card"><span class="service-title">24/7 AI Assistance</span>Instantly handle 70% of customer inquiries.</div>
                <div class="service-card"><span class="service-title">Reputation Management</span>Dominate local rankings on Google Maps.</div>
                <div class="service-card"><span class="service-title">Workflow Automation</span>Eliminate manual tasks with RAG-based AI solutions.</div>
                <p>Our "One-Time Ownership" model means you own the technology we build for you, delivering permanent ROI without monthly fees.</p>
                <div class="cta"><a href="https://calendly.com/imsunnystark/30min" class="cta-button">Schedule an ROI Consultation</a></div>
                <p>Best regards,<br>
                <strong>{sender_name}</strong><br>
                <a href="https://www.linkedin.com/company/moonlitarc" style="color: {primary_blue}; text-decoration: none; font-size: 13px;">LinkedIn</a> | <a href="https://moonlitarc.vercel.app/" style="color: {primary_blue}; text-decoration: none; font-size: 13px;">Website</a></p>
            </div>
            <div class="social-footer">
                <a href="https://moonlitarc.vercel.app/" class="social-icon"><img src="https://cdn-icons-png.flaticon.com/512/1006/1006771.png" alt="Website"></a>
                <a href="https://www.instagram.com/moonlitarc_ai/" class="social-icon"><img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram"></a>
                <a href="https://www.facebook.com/moonlitarc" class="social-icon"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook"></a>
                <a href="https://x.com/moonlitarc09" class="social-icon"><img src="https://cdn-icons-png.flaticon.com/512/5968/5968958.png" alt="X"></a>
                <a href="https://www.linkedin.com/company/moonlitarc" class="social-icon"><img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" alt="LinkedIn"></a>
                <div class="footer-text"><strong style="color: {primary_blue};">MoonLIT Arc</strong><br>Automate. Innovate. Elevate.<br>&copy; 2026 All rights reserved.</div>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} | MoonLIT Arc <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = f"ROI Analysis and AI Automation for {business_name}"
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
            print(f"Email successfully sent to {to_email}!")
            return True
    except Exception as e:
        print(f"Failed to send email via Gmail SMTP: {e}")
        return False

if __name__ == "__main__":
    # Test send to confirm signature links
    test_email = "imsunnystark@gmail.com"
    send_sales_email(test_email, "Internal Test", "low reviews")
