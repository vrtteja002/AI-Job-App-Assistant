import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM

class EmailSender:
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = EMAIL_PORT
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD
        self.from_email = EMAIL_FROM
        
        # Check if email settings are configured
        self.is_configured = all([
            self.host, self.port, self.username, self.password, self.from_email
        ])
        
        if not self.is_configured:
            print("Email settings are not fully configured. Check your .env file.")
    
    def send_email(self, to_email, subject, body_text, body_html=None, attachments=None):
        """
        Send an email with optional HTML and attachments
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body_text (str): Plain text email body
            body_html (str, optional): HTML email body
            attachments (list, optional): List of file paths to attach
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not self.is_configured:
            print("Email settings are not configured. Cannot send email.")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach text part
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)
            
            # Attach HTML part if provided
            if body_html:
                part2 = MIMEText(body_html, 'html')
                msg.attach(part2)
            
            # Attach files if provided
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as f:
                            file_attachment = MIMEApplication(f.read())
                        
                        file_name = os.path.basename(file_path)
                        file_attachment.add_header('Content-Disposition', 
                                                'attachment', 
                                                filename=file_name)
                        msg.attach(file_attachment)
                    else:
                        print(f"Attachment not found: {file_path}")
            
            # Connect to server and send
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_application_email(self, to_email, subject, body_text, resume_path, cover_letter_path=None):
        """
        Send a job application email with resume and optional cover letter
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body_text (str): Email body
            resume_path (str): Path to resume file
            cover_letter_path (str, optional): Path to cover letter file
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        attachments = [resume_path]
        
        if cover_letter_path:
            attachments.append(cover_letter_path)
            
        return self.send_email(to_email, subject, body_text, attachments=attachments)
    
    def send_follow_up_email(self, to_email, subject, body_text):
        """
        Send a follow-up email
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body_text (str): Email body
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        return self.send_email(to_email, subject, body_text)
