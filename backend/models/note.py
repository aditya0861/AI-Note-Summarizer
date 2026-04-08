from datetime import datetime
from models.database import db


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    summaries = db.relationship("Summary", backref="note", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "filename": self.filename,
            "created_at": self.created_at.isoformat(),
        }
