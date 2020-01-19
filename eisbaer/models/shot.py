from models import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

#
# class Assist(db.Model):
#     __tablename__ = 'assist'
#     id = db.Column(UUID(as_uuid=True), unique=True,
#                    nullable=False, default=uuid4, primary_key=True)
#     shot_id = db.Column(UUID(as_uuid=True), db.ForeignKey('shot.id'))
#     player_id = db.Column(db.Integer(), db.ForeignKey('player.id'))


class Shot(db.Model):
    __tablename__ = 'shot'
    id = db.Column(UUID(as_uuid=True), unique=True,
                   nullable=False, default=uuid4, primary_key=True)
    shot_result = db.Column(db.String(), nullable=False)
    goalie_id = db.Column(db.Integer(), db.ForeignKey('player.id'), nullable=True)
    blocker_id = db.Column(db.Integer(), db.ForeignKey('player.id'), nullable=True)
    # goalie = relationship('Player')
    shooter_id = db.Column(db.Integer(), db.ForeignKey('player.id'), nullable=True)
    # scorer = relationship('Player')
    # assists = relationship('Player', secondary=Assist)
    secondary_type = db.Column(db.String(), nullable=True)
    scored = db.Column(db.Boolean(), nullable=False)
