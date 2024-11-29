import sendgrid
from sendgrid.helpers.mail import Mail
from decouple import config

def send_email(subject, message, recipient_email):
    sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
    email = Mail(
        from_email='vaikunthpatel67@gmail.com',  # Replace with a verified sender
        to_emails=recipient_email,
        subject=subject,
        html_content=message,
    )
    try:
        response = sg.send(email)
        print(f"Email sent successfully: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email to this recipient: {str(e)}")
        return False
