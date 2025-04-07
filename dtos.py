from datetime import datetime
from typing import Optional
from typing import Generic, TypeVar
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
class RecipientReaderDTO:
    id: int
    phone: str


@dataclass
class CampaignCreatorDTO:
    name: str
    phone: str
    call_date: datetime
    recipients: list[str]


@dataclass
class CampaignReaderDTO:
    id: int
    name: str
    phone: str
    call_date: datetime
    recipients: list[RecipientReaderDTO]


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
class QueueCreatorDTO:
    recipient_id: int
    campaign_id: int
    status: str
    scheduled_time: datetime


@dataclass
class QueueUpdaterDTO:
    status: str
    last_attempt_time: datetime
    attempt_count: int


@dataclass
class NotificationCreatorDTO:
    recipient_id: int
    campaign_id: int
    send_time: datetime
    status: str
