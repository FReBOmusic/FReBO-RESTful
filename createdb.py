from FReBOApp import app
from extensions import db
from click import echo

@app.cli.command()
def createdb():
    # initialize the database
    db.create_all()
    echo("FReBO Database created.")
