from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from sqlalchemy.schema import DDL
from sqlalchemy.event import listen

from config import get_settings
from models import NotificationDB
from base_model import Base

SETTING = get_settings()

POSTGRES_HOST = SETTING.postgres_host
POSTGRES_USER = SETTING.postgres_user
POSTGRES_PASSWORD = SETTING.postgres_password
POSTGRES_NAME = SETTING.postgres_db
POSTGRES_PORT = SETTING.postgres_port

# Construct the database URL dynamically
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]

def init_db():
    Base.metadata.create_all(bind=engine)

    setup_database_event_listeners()


def setup_database_event_listeners():
    create_trigger_function = DDL(
        """
        CREATE OR REPLACE FUNCTION check_recent_notification()
        RETURNS TRIGGER AS $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM notifications 
                WHERE recipient_id = NEW.recipient_id 
                AND send_time > (NOW() - INTERVAL '5 minutes')
            ) THEN
                RAISE EXCEPTION 'Duplicate notification for recipient within 5 minutes';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """
    )

    create_trigger = DDL(
        """
        CREATE TRIGGER prevent_duplicate_notifications
        BEFORE INSERT ON notifications
        FOR EACH ROW EXECUTE FUNCTION check_recent_notification();
    """
    )

    listen(NotificationDB.__table__, "after_create", create_trigger_function)
    listen(NotificationDB.__table__, "after_create", create_trigger)
