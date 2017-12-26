import os

class Config(object):
    # Base Configurations

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    #SQLALCHEMY_DATABASE_URI = mysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
    SECRET_KEY = 'thisisthesecretkeythatwillneedtobechangedforproduction'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
