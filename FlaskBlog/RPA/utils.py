from flask_mail import Message
from FlaskBlog import mail

def send_email(adress):

    msg = Message('Your RPA idea!!!',
                  sender='msshubna@gmail.com',
                  recipients=[adress])
    msg.body = f'''BLA BLA  '''

    mail.send(msg)

