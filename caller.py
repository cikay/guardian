from datetime import datetime, timezone
import logging
import asyncio
import random
import time

from dtos import (
    QueueFilterSet,
    ComparisonOperatorSet,
    NotificationCreatorDTO,
    QueueUpdaterDTO,
)
from use_case_factories import (
    QueueListerUseCaseFactory,
    NotificationCreatorUseCaseFactory,
    QueueUpdaterUseCaseFactory,
)
from entities import QueueEntity

logger = logging.getLogger(__name__)


class Caller:
    def __init__(self, session):
        self.session = session
        self.notification_creator_use_case = NotificationCreatorUseCaseFactory.create(
            self.session
        )
        self.queue_lister_use_case = QueueListerUseCaseFactory.create(self.session)
        self.queue_updater_use_case = QueueUpdaterUseCaseFactory.create(self.session)

    def call(self):
        queues = self.queue_lister_use_case.execute(
            QueueFilterSet(
                status=ComparisonOperatorSet(in_=["pending", "failed", "busy"]),
                scheduled_time=ComparisonOperatorSet(lte=datetime.now()),
            )
        )
        for queue in queues:
            logger.info(f"Queue status: {queue.status}")
        if not queues:
            logger.info("No pending queues found.")
            return

        logger.info(f"Pending queues length: {len(queues)}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            asyncio.gather(
                *[self._simulate_call(queue) for queue in queues],
                return_exceptions=True,
            )
        )
        logger.info(f"Simulation results: {result}")
        if result:
            raise Exception("Error occurred during call simulation.")

    async def _simulate_call(self, queue: QueueEntity):
        logger.info(f"type of queue:  {type(queue)}")

        random_int = random.randint(10, 30)
        logger.info(f"Waiting for {random_int} seconds for simulating call.")
        await asyncio.sleep(random_int)
        random_status = random.choice(["answered", "canceled", "busy", "not_reached"])
        update_queue_fields = {
            "last_attempt_time": datetime.now(timezone.utc),
            # This should be done in db level for simplicity i keep as is
            "attempt_count": queue.attempt_count + 1,
        }

        try:
            self.notification_creator_use_case.execute(
                NotificationCreatorDTO(
                    recipient_id=queue.recipient_id,
                    campaign_id=queue.campaign_id,
                    status=random_status,
                    send_time=datetime.now(timezone.utc),
                )
            )
            if random_status == "answered":
                update_queue_fields["status"] = "completed"
                logger.info(f"Call answered for: {queue.recipient}")
            elif random_status in {"canceled", "not_reached", "busy"}:
                update_queue_fields["status"] = "failed"
                logger.info(f"Call failed for: {queue.recipient}")
        except Exception as e:
            logger.error(f"Error creating notification for {queue.recipient}: {e}")
            update_queue_fields["status"] = "busy"

        update_queue = QueueUpdaterDTO(**update_queue_fields)

        self.queue_updater_use_case.execute(queue.id, update_queue)

        logger.info(f"Call simulation completed for: {queue.recipient}")
