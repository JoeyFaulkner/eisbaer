from models import db


class Division(db.Model):
    __tablename__ = 'division'
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)  # same as nhl.com
    nhl_link = db.Column(db.String(), unique=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)
    name_short = db.Column(db.String(), unique=True, nullable=False)
