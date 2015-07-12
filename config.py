import os

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.dirname(__file__)) + '/korform2.db'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///korform2'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True

