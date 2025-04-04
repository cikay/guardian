from dataclasses import asdict, fields


from sqlalchemy import select
from sqlalchemy.orm import Session

from models import CampaignDB, RecipientDB, QueueDB, NotificationDB
from dtos import (
    CampaignCreate,
    QueueQuery,
    UNSET,
    QueueCreate,
    NotificationCreate,
    CampaignQuery,
    QueueUpdate,
)
from entities import CampaignEntity, RecipientEntity, QueueEntity, NotificationEntity


OPERATION_MAPPING = {
    "eq": lambda x, y: x == y,
    "ne": lambda x, y: x != y,
    "gt": lambda x, y: x > y,
    "gte": lambda x, y: x >= y,
    "lt": lambda x, y: x < y,
    "lte": lambda x, y: x <= y,
    "in_": lambda x, y: x.in_(y),
}


class BaseRepository:
    db_model = None

    def __init__(self, session: Session):
        self.session = session

    def _build_query(self, query: dict) -> select:
        filters = []
        for key, value in query.items():
            if value is UNSET:
                continue

            if isinstance(value, dict):
                filters.extend(self._build_field_filters(key, value))
            else:
                filters.append(getattr(self.__class__.db_model, key) == value)

        return self.session.query(self.__class__.db_model).filter(*filters)

    def _build_field_filters(self, field: str, operators: dict) -> select:
        filters = []

        for key, value in operators.items():
            if value is UNSET:
                continue

            func = OPERATION_MAPPING[key]
            filter = func(getattr(self.__class__.db_model, field), value)
            filters.append(filter)

        return filters

    def _get_dataclass_fields_name(self, entity):
        return {field.name for field in fields(entity)}


class CampaignRepository(BaseRepository):
    db_model = CampaignDB

    def __init__(self, session: Session):
        self.session = session

    def create(self, campaign_create: CampaignCreate) -> CampaignEntity:
        recipient_objects = (
            self.session.execute(
                select(RecipientDB).where(
                    RecipientDB.id.in_(campaign_create.recipients)
                )
            )
            .scalars()
            .all()
        )
        campaign_db = CampaignDB(
            name=campaign_create.name,
            phone=campaign_create.phone,
            call_date=campaign_create.call_date,
            recipients=recipient_objects,
        )
        self.session.add(campaign_db)
        self.session.commit()
        self.session.refresh(campaign_db)
        return self._to_entity(campaign_db)

    def get_many(self, query: CampaignQuery) -> list[CampaignEntity]:
        query = self._build_query(asdict(query))
        return [self._to_entity(campaign) for campaign in query.all()]

    def _to_entity(self, campaign_db: CampaignDB) -> CampaignEntity:
        recipient_repo = RecipientRepository(self.session)

        return CampaignEntity(
            id=campaign_db.id,
            name=campaign_db.name,
            phone=campaign_db.phone,
            call_date=campaign_db.call_date,
            recipients=[
                recipient_repo._to_entity(recipient)
                for recipient in campaign_db.recipients
            ],
        )


class RecipientRepository(BaseRepository):
    db_model = RecipientDB

    def __init__(self, session: Session):
        self.session = session

    def get_or_create_many(self, phones: list[str]) -> list[RecipientEntity]:
        "Get if exists, create if not exists for many recipients"
        stmt = select(RecipientDB).where(RecipientDB.phone.in_(phones))
        existing_recipients = self.session.execute(stmt).scalars().all()

        existing_phones = {r.phone for r in existing_recipients}
        new_phones = set(phones) - existing_phones

        if not new_phones:
            return existing_recipients

        new_recipients = [RecipientDB(phone=phone) for phone in new_phones]
        self.session.add_all(new_recipients)
        self.session.commit()

        stmt = select(RecipientDB).where(RecipientDB.phone.in_(new_phones))
        newly_created_recipients = self.session.execute(stmt).scalars().all()
        all_recipients = existing_recipients + list(newly_created_recipients)
        return [self._to_entity(recipient) for recipient in all_recipients]

    def _to_entity(self, recipient_db: RecipientDB) -> RecipientEntity:
        return RecipientEntity(id=recipient_db.id, phone=recipient_db.phone)


class QueueRepository(BaseRepository):
    db_model = QueueDB

    def get(self, query: QueueQuery) -> QueueDB | None:
        query = self._build_query(query)
        return query.first()

    def create(self, queue_create: QueueCreate) -> QueueDB:
        queue_item = QueueDB(**asdict(queue_create))
        self.session.add(queue_item)
        self.session.commit()
        return self._to_entity(queue_item)

    def update(self, queue_id: int, queue_update: QueueUpdate) -> QueueEntity:
        queue_item = self.session.query(QueueDB).get(queue_id)
        if not queue_item:
            return None

        for field in fields(QueueUpdate):
            field_value = getattr(queue_update, field.name)
            if field_value is not UNSET:
                setattr(queue_item, field.name, field_value)

        self.session.commit()
        return self._to_entity(queue_item)

    def get_many(
        self, query: QueueQuery, order_by: str | None = None
    ) -> QueueDB | None:
        query = self._build_query(asdict(query))
        if order_by:
            query = query.order_by(getattr(QueueDB, order_by))
        return [self._to_entity(queue) for queue in query.all()]

    def update_status(self, queue_id: int, status: str):
        queue_item = self.get(queue_id)
        if queue_item:
            queue_item.status = status
            self.session.commit()

    def create_many(self, queue_entries: list):
        queue_objects = []
        for entry in queue_entries:
            queue_objects.append(QueueDB(**entry))

        self.session.add_all(queue_objects)
        self.session.commit()

    def _to_entity(self, queue_db: QueueDB) -> dict:
        fields_name = self._get_dataclass_fields_name(QueueEntity)
        return QueueEntity(**{field: getattr(queue_db, field) for field in fields_name})


class NotificationRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, notification_create: NotificationCreate) -> NotificationEntity:
        notification_db = NotificationDB(**asdict(notification_create))
        self.session.add(notification_db)
        self.session.commit()
        return self._to_entity(notification_db)

    def _to_entity(self, notification_db: NotificationDB) -> NotificationEntity:
        return NotificationEntity(
            id=notification_db.id,
            recipient_id=notification_db.recipient_id,
            campaign_id=notification_db.campaign_id,
            send_time=notification_db.send_time,
            status=notification_db.status,
        )
