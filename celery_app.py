from datetime import timedelta
import time

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import psycopg2

from config import get_settings
from db_setup import get_session, init_db, engine
from caller import Caller

logger = logging.getLogger(__name__)


SETTING = get_settings()


celery_instance = Celery(
    __name__,
    broker=SETTING.celery_broker_url,
    backend=SETTING.celery_result_backend,
)


@worker_process_init.connect
def init_worker(**kwargs):
    init_db()


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    engine.dispose()


@celery_instance.task(name="celery_app.task_process_notification_queue")
def task_process_notification_queue():
    session = next(get_session())
    try:
        Caller(session).call()
    except psycopg2.errors.NumericValueOutOfRange as e:
        logger.error(f"Numeric value out of range: {e}")
        session.rollback()  # Rollback the session
    except (IntegrityError, SQLAlchemyError) as e:
        logger.error(f"SQLAlchemy or Integrity Error: {e}")
        session.rollback()
    except Exception as e:
        logger.error(f"Error in task_process_notification_queue: {e}")
        session.rollback()
    finally:
        session.close()


celery_instance.conf.beat_schedule = {
    "daily-report": {
        "task": "celery_app.task_process_notification_queue",
        "schedule": timedelta(minutes=1),
    },
}
