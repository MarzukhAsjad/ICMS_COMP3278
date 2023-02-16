import smtplib
import email
import ssl

from email.message import EmailMessage



def email():

    # SSL
    port = 465
    smtp_server = "smtp.gmail.com"

    sender_email = 'icms.comp3278@gmail.com'
    # QUERY: SELECT student email
    # ----------- TO BE IMPLEMENTED ------------
    receiver_email = ''
    password = input("Type password: ")

    message = """\
    Subject: Upcoming class information

    """

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(receiver_email, password)
        server.sendmail(sender_email, receiver_email, message)
