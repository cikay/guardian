from datetime import datetime, timedelta
import asyncio
import random

from dtos import QueueQuery, ComparisonOperators

from controller_factories import ListQueueUseCaseFactory
from celery_app import get_celery_db_session


async def simulate_call(recipient_phone: str):
    print(f"Arama simülasyonu başlatıldı: {recipient_phone}")
    random_int = random.randint(0, 30)
    await asyncio.sleep(random_int)


    durumlar = ["answered", "canceled", "busy"]
    return random.choice(durumlar)


def process_notification_queue():
    session = next(get_celery_db_session())
    list_queue_use_case = ListQueueUseCaseFactory.create(session)

    scheduled_time = ComparisonOperators(lte=datetime.now())
    query = QueueQuery(status="pending", scheduled_time=scheduled_time)
    queue_entries = list_queue_use_case.execute(query)
