from models import CampaignDB
from entities import CampaignEntity
from dataclasses import asdict
from entities import RecipientEntity, QueueEntity, NotificationEntity
from models import RecipientDB, QueueDB, NotificationDB


class RecipientEntityModelMapper:
    @staticmethod
    def to_entity(recipient_model: RecipientDB) -> RecipientEntity:
        return RecipientEntity(
            id=recipient_model.id,
            phone=recipient_model.phone,
        )

    @staticmethod
    def to_model(recipient_domain: RecipientEntity) -> RecipientDB:
        domain_dict = asdict(recipient_domain)
        return RecipientDB(**domain_dict)


class CampaignEntityModelMapper:
    @staticmethod
    def to_entity(campaign_model: CampaignDB) -> CampaignEntity:
        return CampaignEntity(
            id=campaign_model.id,
            name=campaign_model.name,
            phone=campaign_model.phone,
            call_date=campaign_model.call_date,
            recipients=[
                RecipientEntityModelMapper.to_entity(recipient)
                for recipient in campaign_model.recipients
            ],
        )

    @staticmethod
    def to_model(campaign_domain: CampaignEntity) -> CampaignDB:
        domain_dict = asdict(campaign_domain)
        return CampaignDB(**domain_dict)


class QueueEntityModelMapper:
    @staticmethod
    def to_entity(queue_model: QueueDB) -> QueueEntity:
        return QueueEntity(
            id=queue_model.id,
            status=queue_model.status,
            scheduled_time=queue_model.scheduled_time,
            recipient_id=queue_model.recipient_id,
            campaign_id=queue_model.campaign_id,
            attempt_count=queue_model.attempt_count,
        )

    @staticmethod
    def to_model(queue_domain: QueueEntity) -> QueueDB:
        domain_dict = asdict(queue_domain)
        return QueueDB(**domain_dict)


class NotificationEntityModelMapper:
    @staticmethod
    def to_entity(notification_model: NotificationDB) -> NotificationEntity:
        return NotificationEntity(
            id=notification_model.id,
            recipient_id=notification_model.recipient_id,
            campaign_id=notification_model.campaign_id,
            send_time=notification_model.send_time,
            status=notification_model.status,
        )

    @staticmethod
    def to_model(notification_domain: NotificationEntity) -> NotificationDB:
        domain_dict = asdict(notification_domain)
        return NotificationDB(**domain_dict)
