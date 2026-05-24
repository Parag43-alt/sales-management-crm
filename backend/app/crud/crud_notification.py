from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate

def get_user_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 50):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

def get_unread_count(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).count()

def create_notification(db: Session, obj_in: NotificationCreate):
    db_obj = Notification(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def mark_as_read(db: Session, notification_id: int, user_id: int):
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if notif:
        notif.is_read = True
        db.commit()
        db.refresh(notif)
    return notif

def delete_notification(db: Session, notification_id: int, user_id: int):
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if notif:
        db.delete(notif)
        db.commit()
    return notif
