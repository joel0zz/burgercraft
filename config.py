# AWS RDS - MariaDB
FLASK_APP='manage.py'
FLASK_ENV='development'
SECRET_KEY="WTFr%#-gs.~^,3Qx*Qyf"
SECURITY_PASSWORD_SALT = '.!3ZjZBDjkxFsGAA4EZ4.Jxn'
DB_USERNAME='burgercraftroot'
DB_PASSWORD="wV3oVp6uVnbR!pAHjdXAN7"
DB_HOST='burgercraft.czb2xkpjsyrf.ap-southeast-2.rds.amazonaws.com'
DATABASE_NAME='burgercraftdb'
DB_URI = "mysql+pymysql://%s:%s@%s:3306/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
BLOG_NAME='burgercraft.'

# SES SMTP settings.
MAIL_SERVER='email-smtp.us-east-1.amazonaws.com'
MAIL_PORT= 587
MAIL_USERNAME = 'AKIA4IB4T3QLTXPAJMEB'
MAIL_PASSWORD = 'BF3aV0qR/RlEowTI3hVg4YTx5Me9qmavZPlmNjmGDDuZ'
MAIL_DEFAULT_SENDER = 'burgermail@burgercraft.org'
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# AWS s3 config
BUCKET_NAME = 'burgercraft-images'
REGION = 's3-ap-southeast-2'