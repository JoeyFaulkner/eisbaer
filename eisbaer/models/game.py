from models import db


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.String(), nullable=False, unique=True, primary_key=True)  # same as nfl.com
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    season = db.Column(db.String(), nullable=False)
    venue = db.Column(db.String(), nullable=True)
    home = db.Column(db.Integer(), db.ForeignKey('team.id'))
    away = db.Column(db.Integer(), db.ForeignKey('team.id'))
    game_type = db.Column(db.String(), nullable=False)
