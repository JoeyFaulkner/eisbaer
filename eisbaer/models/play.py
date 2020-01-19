from models import db
from geoalchemy2 import Geometry
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

# some relation between plays and players


class Play(db.Model):
    __tablename__ = 'play'
    id = db.Column(db.Integer(), unique=True, primary_key=True)  # same as nhl.com
    game_id = db.Column(db.String(), db.ForeignKey('game.id'), nullable=False)
    period_clock = db.Column(db.Time(), nullable=False)
    period = db.Column(db.Integer(), nullable=False)
    period_type = db.Column(db.String(), nullable=False)
    position = db.Column(Geometry('POINT'), nullable=True)
    description = db.Column(db.String(), nullable=True)
    event_code = db.Column(db.String(), nullable=True)
    faceoff_id = db.Column(UUID(as_uuid=True), db.ForeignKey('faceoff.id'), nullable=True)
    shot_id = db.Column(UUID(as_uuid=True), db.ForeignKey('shot.id'), nullable=True)
