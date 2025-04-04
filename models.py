from datetime import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey, Table, Column, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from base_model import Base
from enums import NotificationStatus, QueueStatus


campaign_recipient = Table(
    "campaign_recipient",
    Base.metadata,
    Column("campaign_id", ForeignKey("campaigns.id"), primary_key=True),
    Column("recipient_id", ForeignKey("recipients.id"), primary_key=True),
)



class RecipientDB(Base):
    __tablename__ = "recipients"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    campaigns: Mapped[list["CampaignDB"]] = relationship(
        secondary=campaign_recipient, back_populates="recipients"
    )
    notifications: Mapped[list["NotificationDB"]] = relationship(
        back_populates="recipient", cascade="all, delete-orphan"
    )
    queue_items: Mapped[list["QueueDB"]] = relationship(
        back_populates="recipient", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<RecipientDB(phone={self.phone})>"


class CampaignDB(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    call_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    recipients: Mapped[list["RecipientDB"]] = relationship(
        secondary=campaign_recipient, back_populates="campaigns"
    )
    notifications: Mapped[list["NotificationDB"]] = relationship(
        back_populates="campaign", cascade="all, delete-orphan"
    )
    queue_items: Mapped[list["QueueDB"]] = relationship(
        back_populates="campaign", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Campaign(name={self.name})>"


class NotificationDB(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipients.id"), nullable=False
    )
    campaign_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("campaigns.id"), nullable=False
    )
    send_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(Enum(NotificationStatus), default="waiting")

    recipient: Mapped["RecipientDB"] = relationship(back_populates="notifications")
    campaign: Mapped["CampaignDB"] = relationship(back_populates="notifications")

    def __repr__(self):
        return f"<NotificationDB(recipient_id={self.recipient_id}, campaign_id={self.campaign_id}, status={self.status})>"



class QueueDB(Base):
    __tablename__ = "queue"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("campaigns.id"), nullable=False
    )
    recipient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipients.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(Enum(QueueStatus), default="pending")
    scheduled_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    last_attempt_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    campaign: Mapped["CampaignDB"] = relationship(back_populates="queue_items")
    recipient: Mapped["RecipientDB"] = relationship(back_populates="queue_items")

    def __repr__(self):
        return (
            f"<QueueDB(campaign_id={self.campaign_id}, recipient_id={self.recipient_id}, "
            f"status={self.status}, scheduled_time={self.scheduled_time})>"
        )
