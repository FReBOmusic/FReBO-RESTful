import datetime as dt
from uuid import uuid4
from FReBOApp import app
from itsdangerous import URLSafeSerializer
from extensions import db, ph, VerificationError
from itsdangerous import BadSignature


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Binary(16), unique=True, nullable=False, default=lambda : uuid4().bytes) # random UUID
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=False) #: The hashed password
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    #session_token = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    session_count = db.Column(db.Integer, default=0)

    def __init__(self, username, email, password, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)
        self.set_password(password)

    def get_token(self):
        serializer = URLSafeSerializer(app.secret_key)
        return serializer.dumps([self.id, self.username, self.password.decode('utf-8'), self.session_count])

    def set_password(self, password):
        """Set password."""
        self.password = str.encode(ph.hash(password)) # storing passwords as binary

    def check_password(self, value):
        """Check password."""
        try:
            return ph.verify(self.password, value)
        except VerificationError:
            return False

    def update_session_count(self):
        self.session_count += 1
        db.session.add(self)
        db.session.commit()

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    @classmethod
    def get_user_from_token(cls, session_token):
        serializer = URLSafeSerializer(app.secret_key)

        try:
            id, user, passwd, session_count = serializer.loads(session_token)
            user = cls.query.filter_by(id=id, username=user, password=str.encode(passwd), session_count=session_count).first()
        except BadSignature:
            return None

        return user.first()

    @classmethod
    def get_user_from_username_or_email(cls, username_or_email):
        user = cls.query.filter_by(username=username_or_email).first()

        if not user:
            # Try email
            user = cls.query.filter_by(email=username_or_email).first()

            if not user:
                return None # user doesn't exist

        return user

    @classmethod
    def username_is_unique(cls, username):
        if cls.query.filter_by(username=username).first() is not None:
            return False
        return True

    @classmethod
    def email_is_unique(cls, email):
        if cls.query.filter_by(email=email).first() is not None:
            return False
        return True


