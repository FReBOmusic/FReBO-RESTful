from flask import g #, abort
from flask_restplus import Resource
from Model.User import User
from extensions import db, api, token_auth, passwd_auth
from schemas import SignupSchema


@passwd_auth.verify_password
def verify_password(username_or_email, password):
    user = User.get_user_from_username_or_email(username_or_email)

    if user is None or not user.check_password(password):
        return False

    g.current_user = user
    return True

@token_auth.verify_token
def verify_token(session_token):
    user = User.get_user_from_token(session_token)

    if user is None:
        return False

    g.current_user = user
    return True

@api.route('/auth/login') #, subdomain='mobile)
class Login(Resource):

    @passwd_auth.login_required
    def get(self):
        user = g.current_user
        user.update_session_count()
        return { 'auth_token': user.get_token() }

@api.route('/auth/signup') #, subdomain='mobile')
class Signup(Resource):

    def post(self):
        schema = SignupSchema()
        data, errors = schema.load(api.payload)

        if errors:
            return errors, 400

        username = data['username']
        email = data['email']

        if not User.username_is_unique(username):
            errors['username'] = ["User already exits."]
        if not User.email_is_unique(email):
            errors['email'] = ["Email already exits."]
        if errors:
            return errors, 403

        password = data['password']
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()

        # try:
        #     db.session.add(user)
        #     db.session.commit()
        # except:
        #     abort(400) # could not create user for some reason
        return {'auth_token': user.get_token()}
