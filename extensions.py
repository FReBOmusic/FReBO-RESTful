from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError as VerificationError
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth #, MultiAuth
from flask_restplus import Api
from flask_marshmallow import Marshmallow

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy()
ma = Marshmallow()
ph = PasswordHasher()
token_auth = HTTPTokenAuth(scheme='Token')
passwd_auth = HTTPBasicAuth(scheme='Basic')
#auth = MultiAuth(token_auth, passwd_auth)
api = Api(doc=False)
