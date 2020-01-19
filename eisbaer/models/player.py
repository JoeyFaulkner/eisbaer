from models import db


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    birth_city = db.Column(db.String(), nullable=True)
    birth_country = db.Column(db.String(), nullable=True)
    birth_date = db.Column(db.DateTime(), nullable=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    nhl_link = db.Column(db.String(), nullable=False)
    nationality = db.Column(db.String(), nullable=False)
    position_abb = db.Column(db.String(), nullable=False)
    position_type = db.Column(db.String(), nullable=False)

    weight = db.Column(db.Integer(), nullable=False)
    shoots_catches = db.Column(db.String(), nullable=False)
