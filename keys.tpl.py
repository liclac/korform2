# -- Security Salts
# 
# It's kinda important that you change these; if an attacker can guess your
# salts, they can do all sorts of nasty stuff that you really don't want.
# 
SECRET_KEY				= 'put something secret here'

SECURITY_PASSWORD_SALT	= 'another secret goes here'
SECURITY_CONFIRM_SALT	= 'a third one here'
SECURITY_RESET_SALT		= 'no reusing salts here'
SECURITY_LOGIN_SALT		= 'and do not forget to change any of them'
SECURITY_REMEMBER_SALT	= 'especially not this one'

# -- Mail server setup
# 
# These are commented (with default values given), because they work just fine
# with the usual recommended setup of having a local mailer daemon forwarding
# to something like Mandrill or Mailgun. Edit if your setup differs.
# 
#MAIL_SERVER 			= 'localhost'
#MAIL_PORT				= 25
#MAIL_USE_TLS			= False
#MAIL_USE_SSL			= False
#MAIL_USERNAME			= None
#MAIL_PASSWORD			= None
