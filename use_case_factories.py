from use_cases import (
    ListQueueUseCase,
    CreateQueueUseCase,
    CreateNotificationUseCase,
    UpdateQueueUseCase,
)
from repositories import QueueRepository, NotificationRepository


class ListQueueUseCaseFactory:
    @staticmethod
    def create(session) -> ListQueueUseCase:
        repo = QueueRepository(session)
        return ListQueueUseCase(repo)


class CreateQueueUseCaseFactory:
    @staticmethod
    def create(session) -> CreateQueueUseCase:
        repo = QueueRepository(session)
        return CreateQueueUseCase(repo)


class CreateNotificationUseCaseFactory:
    @staticmethod
    def create(session) -> CreateNotificationUseCase:
        repo = NotificationRepository(session)
        return CreateNotificationUseCase(repo)


class UpdateQueueUseCaseFactory:
    @staticmethod
    def create(session) -> UpdateQueueUseCase:
        repo = QueueRepository(session)
        return UpdateQueueUseCase(repo)
