from datetime import datetime
from typing import Optional
from typing import Generic, TypeVar, Literal
from dataclasses import dataclass


UNSET = type("UNSET", (), {})

T = TypeVar("T")


@dataclass
class ComparisonOperators(Generic[T]):
    in_: Optional[list[T]] = UNSET
    eq: Optional[T] = UNSET
    neq: Optional[T] = UNSET
    gt: Optional[T] = UNSET
    lt: Optional[T] = UNSET
    gte: Optional[T] = UNSET
    lte: Optional[T] = UNSET


@dataclass
class RecipientRead:
    id: int
    phone: str


@dataclass
class CampaignCreate:
    name: str
    phone: str
    call_date: datetime
    recipients: list[str]


@dataclass
class CampaignRead:
    id: int
    name: str 
    phone: Literal["1234567890", "9876543210", "5551234567"]
    call_date: datetime
    recipients: list["RecipientRead"]


@dataclass
class RecipientQuery:
    id: int | ComparisonOperators | UNSET = UNSET
    phone: str | ComparisonOperators | UNSET = UNSET


@dataclass
class CampaignQuery:
    id: int | ComparisonOperators | UNSET = UNSET
    name: str | ComparisonOperators | UNSET = UNSET
    phone: str | ComparisonOperators | UNSET = UNSET
    call_date: datetime | ComparisonOperators | UNSET = UNSET
    recipient: Optional["RecipientQuery"] = UNSET


@dataclass
class QueueQuery:
    id: int | ComparisonOperators = UNSET
    status: str | ComparisonOperators[str] = UNSET
    scheduled_time: datetime | ComparisonOperators[datetime] = UNSET


@dataclass
class QueueCreate:
    recipient_id: int
    campaign_id: int
    status: str
    scheduled_time: datetime


@dataclass
class QueueUpdate:
    status: str
    last_attempt_time: datetime
    attempt_count: int


@dataclass
class NotificationCreate:
    recipient_id: int
    campaign_id: int
    send_time: datetime
    status: str
