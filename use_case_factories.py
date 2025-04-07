from use_cases import (
    QueueListerUseCase,
    QueueCreatorUseCase,
    NotificationCreatorUseCase,
    QueueUpdaterUseCase,
)
from repositories import QueueRepository, NotificationRepository


class QueueListerUseCaseFactory:
    @staticmethod
    def create(session) -> QueueListerUseCase:
        repo = QueueRepository(session)
        return QueueListerUseCase(repo)


class QueueCreatorUseCaseFactory:
    @staticmethod
    def create(session) -> QueueCreatorUseCase:
        repo = QueueRepository(session)
        return QueueCreatorUseCase(repo)


class NotificationCreatorUseCaseFactory:
    @staticmethod
    def create(session) -> NotificationCreatorUseCase:
        repo = NotificationRepository(session)
        return NotificationCreatorUseCase(repo)


class QueueUpdaterUseCaseFactory:
    @staticmethod
    def create(session) -> QueueUpdaterUseCase:
        repo = QueueRepository(session)
        return QueueUpdaterUseCase(repo)
