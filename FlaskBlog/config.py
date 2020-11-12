import os

class Config:
    SECRET_KEY = '4f7872c50669c36dbf73ea07dee32da1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME ='shubnatest@gmail.com'  # os.environ.get('EMAIL_USER')
    MAIL_PASSWORD ='ncbuhtyxsbeqsnsn'  # os.environ.get('EMAIL_PASS')

    #MAIL_USERNAME = os.environ.get('EMAIL_USER')
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
