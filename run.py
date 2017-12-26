""" Special Thanks to Steven Loria's [cookiecuttter-flask](https://github.com/sloria/cookiecutter-flask.git) template for organizational ideas! """

import sys
from FReBOApp import app

if __name__ == '__main__':
    # if 'createdb' in sys.argv:
    #     with app.app_context():
    #         db.create_all()
    #     print("Database created: 'test.db'")
    app.run(debug=True)
