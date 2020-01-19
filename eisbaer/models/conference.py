from models import db


class Conference(db.Model):
    __tablename__ = 'conference'
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)  # same as nhl.com
    nhl_link = db.Column(db.String(), unique=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)