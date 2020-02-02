import os

class Config:
	SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
	SECRET_KEY = "9be8f28f87c515b14ea6bf8a647fdcf5"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = "akashraj5399@gmail.com"
	MAIL_PASSWORD = "vgdvirbrjdlakbky"