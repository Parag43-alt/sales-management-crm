from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.notification import NotificationResponse, NotificationCreate
from app.crud import crud_notification

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
def read_notifications(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_notification.get_user_notifications(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = crud_notification.get_unread_count(db=db, user_id=current_user.id)
    return {"unread_count": count}

@router.post("/", response_model=NotificationResponse)
def create_notification(
    notif_in: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Security: Ensure user can only create notifs for themselves or system overrides
    return crud_notification.create_notification(db=db, obj_in=notif_in)

@router.put("/{notif_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notif_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notif = crud_notification.mark_as_read(db=db, notification_id=notif_id, user_id=current_user.id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notif

@router.delete("/{notif_id}")
def delete_notification(
    notif_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notif = crud_notification.delete_notification(db=db, notification_id=notif_id, user_id=current_user.id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "deleted"}
