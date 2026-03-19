import os
import logging
import smtplib

from dotenv import load_dotenv

from src.models.fixplan import FixPlan
from src.models.incident import Incident
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Notifier:
    def __init__(self):
        self.SMTP_HOST = os.getenv("SMTP_HOST")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT"))
        self.SMTP_USER = os.getenv("SMTP_USER")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
        self.ALERT_EMAIL = os.getenv("ALERT_EMAIL")
        self.WARDEN_URL = os.getenv("WARDEN_URL")

    async def send_alert_email(self, incident: Incident, fixplan: FixPlan):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚨 Warden Alert: {incident.container_name}"
        msg["From"] = self.SMTP_USER
        msg["To"] = self.ALERT_EMAIL
        body = self._build_email_body(incident, fixplan)
        msg.attach(MIMEText(body, "html"))

        try:
            # Connect to the SMTP server
            # We use a 'with' statement to ensure the connection is automatically closed
            with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT) as server:
                server.starttls()  # Secure the connection with TLS
                server.login(self.SMTP_USER, self.SMTP_PASSWORD)
                server.sendmail(self.SMTP_USER, [self.ALERT_EMAIL], msg.as_string())
            logger.info(
                f"Email sent successfully to {self.ALERT_EMAIL} with subject: {msg['Subject']}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send email. Error: {e}")
            return False

    def _build_email_body(self, incident: Incident, fixplan: FixPlan) -> str:
        approve_url = f"{self.WARDEN_URL}/approve/{fixplan.id}"
        reject_url = f"{self.WARDEN_URL}/reject/{fixplan.id}"

        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">

            <h2 style="color: #e74c3c;">🚨 Warden Alert</h2>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr style="background: #f8f9fa;">
                    <td style="padding: 10px; font-weight: bold;">Container</td>
                    <td style="padding: 10px;">{incident.container_name}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Anomaly</td>
                    <td style="padding: 10px;">{incident.crash_reason}</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 10px; font-weight: bold;">Severity</td>
                    <td style="padding: 10px;">{incident.severity.value.upper()}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Time</td>
                    <td style="padding: 10px;">{incident.timestamp}</td>
                </tr>
            </table>

            <h3 style="color: #2c3e50;">🤖 AI Analysis</h3>
            <p><strong>Root Cause:</strong> {fixplan.root_cause}</p>
            <p><strong>Suggested Fix:</strong> {fixplan.explanation}</p>
            <p><strong>Action:</strong> {fixplan.action}</p>

            <h3 style="color: #2c3e50;">⚡ Approve Fix?</h3>
            <p>
                <a href="{approve_url}" 
                   style="background:#27ae60; color:white; padding:12px 24px; 
                          text-decoration:none; border-radius:4px; margin-right:10px;">
                    ✅ Approve Fix
                </a>
                <a href="{reject_url}" 
                   style="background:#e74c3c; color:white; padding:12px 24px; 
                          text-decoration:none; border-radius:4px;">
                    ❌ Reject
                </a>
            </p>

            <hr style="margin-top: 30px;">
            <p style="color: #999; font-size: 12px;">
                Warden — A system that guards your containers
            </p>

        </body>
        </html>
        """
