from datetime import datetime, timezone

from exceptions import CustomException
from repositories import (
    CampaignRepository,
    RecipientRepository,
    QueueRepository,
    NotificationRepository,
)
from dtos import CampaignCreate, QueueQuery, QueueCreate, NotificationCreate
from entities import CampaignEntity


class CampaignCreateUseCase:

    def __init__(
        self,
        campaign_repository: CampaignRepository,
        recipient_repository: RecipientRepository,
    ):
        self.campaign_repository = campaign_repository
        self.recipient_repository = recipient_repository

    def execute(self, campaign_create: CampaignCreate) -> CampaignEntity:
        errors = self._validate(campaign_create)
        if errors:
            raise CustomException(errors)

        recipients = self.recipient_repository.get_or_create_many(
            campaign_create.recipients
        )

        campaign_create.recipients = [recipient.id for recipient in recipients]

        campaign_entity = self.campaign_repository.create(campaign_create)
        self._create_queues(campaign_entity)
        return campaign_entity

    def _create_queues(self, campaign_entity: CampaignEntity):
        from use_case_factories import CreateQueueUseCaseFactory

        create_queue_case = CreateQueueUseCaseFactory.create(
            self.campaign_repository.session
        )

        for recipient in campaign_entity.recipients:
            queue = QueueCreate(
                recipient_id=recipient.id,
                campaign_id=campaign_entity.id,
                status="pending",
                scheduled_time=campaign_entity.call_date,
            )
            create_queue_case.execute(queue)

    def _validate(self, campaign_create) -> set[str]:
        errors = set()
        if campaign_create.call_date < datetime.now(timezone.utc):
            errors.add("Campaign date must be in the future")

        if not campaign_create.phone.isdigit():
            errors.add("Phone number must contain only digits")

        if len(campaign_create.phone) != 11:
            errors.add("Phone number must be exactly 11 digits long")

        recipient_errors = self._validate_recipients(campaign_create.recipients)
        if recipient_errors:
            errors = errors.union(recipient_errors)

        return errors

    def _validate_recipients(self, recipients: list[str]) -> set[str]:
        errors = set()
        for recipient in recipients:
            if not recipient.isdigit():
                errors.add(f"Recipient phone {recipient} must contain only digits")
            if len(recipient) != 11:
                errors.add(
                    f"Recipient phone {recipient} must be exactly 11 digits long"
                )

        return errors


class CampaignListUseCase:

    def __init__(self, campaign_repository: CampaignRepository):
        self.campaign_repository = campaign_repository

    def execute(self, campaign):
        return self.campaign_repository.get_many(campaign)


class ListQueueUseCase:
    def __init__(self, queue_repo: QueueRepository):
        self.queue_repo = queue_repo

    def execute(self, query: QueueQuery):
        return self.queue_repo.get_many(query)


class CreateQueueUseCase:
    def __init__(self, queue_repo: QueueRepository):
        self.queue_repo = queue_repo

    def execute(self, queue: QueueCreate):
        return self.queue_repo.create(queue)


class UpdateQueueUseCase:
    def __init__(self, queue_repo: QueueRepository):
        self.queue_repo = queue_repo

    def execute(self, queue_id: int, queue: QueueCreate):
        return self.queue_repo.update(queue_id, queue)


class CreateNotificationUseCase:
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def execute(self, notification: NotificationCreate):
        return self.notification_repo.create(notification)
