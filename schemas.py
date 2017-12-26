from extensions import ma

class SignupSchema(ma.Schema):
    username = ma.String(required=True)
    email = ma.Email(required=True)
    password = ma.String(required=True)
