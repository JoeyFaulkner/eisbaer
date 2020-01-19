from models import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

# some relation between plays and players


class Faceoff(db.Model):
    __tablename__ = 'faceoff'
    id = db.Column(UUID(as_uuid=True), unique=True,
                   nullable=False, default=uuid4, primary_key=True)
    winning_player_id = db.Column(db.Integer(), db.ForeignKey('player.id'))
    # winning_player = relationship('Player')
    losing_player_id = db.Column(db.Integer(), db.ForeignKey('player.id'))
    # losing_player = relationship('Player')
