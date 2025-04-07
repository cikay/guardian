from datetime import datetime, timezone

from exceptions import CustomException
from dtos import (
    CampaignCreatorDTO,
    QueueFilterSet,
    QueueCreatorDTO,
    NotificationCreatorDTO,
)
from entities import CampaignEntity
from repository_protocols import RepositoryProtocol


class QueueCreatorUseCase:

    def __init__(self, queue_repo: RepositoryProtocol):
        self.queue_repo = queue_repo

    def execute(self, queue: QueueCreatorDTO):
        return self.queue_repo.create(queue)


class CampaignCreatorUseCase:

    def __init__(
        self,
        campaign_repository: RepositoryProtocol,
        recipient_repository: RepositoryProtocol,
        create_queue_case: QueueCreatorUseCase,
    ):
        self.campaign_repository = campaign_repository
        self.recipient_repository = recipient_repository
        self.create_queue_case = create_queue_case

    def execute(self, campaign_create: CampaignCreatorDTO) -> CampaignEntity:
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
        for recipient in campaign_entity.recipients:
            queue = QueueCreatorDTO(
                recipient_id=recipient.id,
                campaign_id=campaign_entity.id,
                status="pending",
                scheduled_time=campaign_entity.call_date,
            )
            self.create_queue_case.execute(queue)

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


class CampaignListerUseCase:

    def __init__(self, campaign_repository: RepositoryProtocol):
        self.campaign_repository = campaign_repository

    def execute(self, campaign):
        return self.campaign_repository.get_many(campaign)


class QueueListerUseCase:

    def __init__(self, queue_repo: RepositoryProtocol):
        self.queue_repo = queue_repo

    def execute(self, query: QueueFilterSet):
        return self.queue_repo.get_many(query)


class QueueUpdaterUseCase:

    def __init__(self, queue_repo: RepositoryProtocol):
        self.queue_repo = queue_repo

    def execute(self, queue_id: int, queue: QueueCreatorDTO):
        return self.queue_repo.update(queue_id, queue)


class NotificationCreatorUseCase:

    def __init__(self, notification_repo: RepositoryProtocol):
        self.notification_repo = notification_repo

    def execute(self, notification: NotificationCreatorDTO):
        return self.notification_repo.create(notification)
