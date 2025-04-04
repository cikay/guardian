import enum


class QueueStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"  # This status is used for completed notifications
    BUSY = "busy"  # There are too many calls in a short time need to wait
    FAILED = "failed" # notification status is any of not reached, busy, canceled


class NotificationStatus(str, enum.Enum):
    SENT = "answered"
    CANCELED = "canceled"
    BUSY = "busy" # The recipient is busy
    NOT_REACHED = "not_reached"
