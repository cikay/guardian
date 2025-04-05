from datetime import datetime
from typing import Optional
from typing import Generic, TypeVar, Literal
from dataclasses import dataclass


UNSET = type("UNSET", (), {})

T = TypeVar("T")


@dataclass
class ComparisonOperatorSet(Generic[T]):
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
    phone: str
    call_date: datetime
    recipients: list[RecipientRead]


@dataclass
class RecipientFilterSet:
    id: int | ComparisonOperatorSet | UNSET = UNSET
    phone: str | ComparisonOperatorSet | UNSET = UNSET


@dataclass
class CampaignFilterSet:
    id: int | ComparisonOperatorSet | UNSET = UNSET
    name: str | ComparisonOperatorSet | UNSET = UNSET
    phone: str | ComparisonOperatorSet | UNSET = UNSET
    call_date: datetime | ComparisonOperatorSet | UNSET = UNSET
    recipient: Optional["RecipientFilterSet"] = UNSET


@dataclass
class QueueFilterSet:
    id: int | ComparisonOperatorSet = UNSET
    status: str | ComparisonOperatorSet[str] = UNSET
    scheduled_time: datetime | ComparisonOperatorSet[datetime] = UNSET


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
