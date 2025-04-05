from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RecipientEntity:
    id: int
    phone: str
    campaigns: list["CampaignEntity"] | None = None


@dataclass
class CampaignEntity:
    id: int
    name: str
    phone: str
    call_date: datetime
    recipients: list["RecipientEntity"]

    # Entity business logic goes here


@dataclass
class QueueEntity:
    id: int
    recipient_id: int
    campaign_id: int
    status: str
    scheduled_time: datetime
    attempt_count: int
    last_attempt_time: Optional[datetime] = None
    recipient: Optional["RecipientEntity"] = None


@dataclass
class NotificationEntity:
    id: int
    recipient_id: int
    campaign_id: int
    send_time: datetime
    status: str
