import logging
from sqlalchemy.orm import joinedload
from models.database import db
from models.note import Note
from models.summary import Summary

logger = logging.getLogger(__name__)


def create_note(content, filename=None):
    try:
        note = Note(content=content, filename=filename)
        db.session.add(note)
        db.session.commit()
        logger.info("Note created id=%d", note.id)
        return note
    except Exception:
        db.session.rollback()
        raise


def get_note_by_id(note_id):
    return db.session.get(Note, note_id)


def save_summary(note_id, summary_type, output):
    try:
        summary = Summary(note_id=note_id, type=summary_type, output=output)
        db.session.add(summary)
        db.session.commit()
        return summary
    except Exception:
        db.session.rollback()
        raise


def get_history(limit=50, offset=0):
    notes = (
        Note.query
        .options(joinedload(Note.summaries))
        .order_by(Note.created_at.desc())
        .limit(limit).offset(offset).all()
    )
    return [{**n.to_dict(), "summaries": [s.to_dict() for s in n.summaries]} for n in notes]
