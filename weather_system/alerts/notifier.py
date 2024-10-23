import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from .threshold_manager import ThresholdAlert

class AlertNotifier:
    def __init__(self, email_config: dict = None):
        self.email_config = email_config or {}
        self.logger = logging.getLogger(__name__)

    def send_email_alert(self, alert: ThresholdAlert):
        """Send email notification for an alert"""
        if not self.email_config:
            self.logger.warning("Email configuration not provided. Skipping email notification.")
            return

        try:
            msg = MIMEMultipart()
            msg['Subject'] = f'Weather Alert: {alert.condition} in {alert.city}'
            msg['From'] = self.email_config.get('sender')
            msg['To'] = self.email_config.get('recipient')

            body = f"""
            Weather Alert!
            
            City: {alert.city}
            Condition: {alert.condition}
            Value: {alert.value:.1f}°C
            Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            """

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                if self.email_config.get('use_tls'):
                    server.starttls()
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
                
            self.logger.info(f"Alert email sent for {alert.city}")
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {str(e)}")

    def console_alert(self, alert: ThresholdAlert):
        """Display alert in console"""
        message = f"""
        🚨 WEATHER ALERT 🚨
        City: {alert.city}
        Condition: {alert.condition}
        Value: {alert.value:.1f}°C
        Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        """
        print(message)
        self.logger.info(f"Alert displayed for {alert.city}")

    def process_alerts(self, alerts: List[ThresholdAlert]):
        """Process multiple alerts"""
        for alert in alerts:
            self.console_alert(alert)
            self.send_email_alert(alert)