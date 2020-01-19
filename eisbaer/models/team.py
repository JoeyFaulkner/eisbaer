from models import db


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer(), unique=True, primary_key=True)  # same as nhl.com
    conference = db.Column(db.Integer(), db.ForeignKey('conference.id'), nullable=False)
    division = db.Column(db.Integer(), db.ForeignKey('division.id'), nullable=False)
    short_name = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    tri_code = db.Column(db.String(), nullable=False)
    nhl_link = db.Column(db.String(), nullable=False, unique=True)
    home_site = db.Column(db.String(), nullable=False, unique=True)
    abbreviation = db.Column(db.String(), nullable=False, unique=True)
