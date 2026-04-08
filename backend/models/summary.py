from datetime import datetime
from models.database import db


class Summary(db.Model):
    __tablename__ = "summaries"

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)
    output = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "note_id": self.note_id,
            "type": self.type,
            "output": self.output,
            "created_at": self.created_at.isoformat(),
        }
