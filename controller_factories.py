from controllers import ListCampaignController, CreateCampaignController
from use_cases import CampaignCreateUseCase, CampaignListUseCase
from repositories import CampaignRepository, RecipientRepository
from use_case_factories import CreateQueueUseCaseFactory


class CreateCampaignControllerFactory:
    @staticmethod
    def create(session) -> CreateCampaignController:
        campaign_repo = CampaignRepository(session)
        recipient_repo = RecipientRepository(session)
        create_queue_case = CreateQueueUseCaseFactory.create(session)
        use_case = CampaignCreateUseCase(
            campaign_repo, recipient_repo, create_queue_case
        )
        return CreateCampaignController(use_case)


class ListCampaignControllerFactory:
    @staticmethod
    def create(session) -> ListCampaignController:
        campaign_repo = CampaignRepository(session)
        use_case = CampaignListUseCase(campaign_repo)
        return ListCampaignController(use_case)
