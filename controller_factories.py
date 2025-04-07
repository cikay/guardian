from controllers import CampaignListerController, CampaignCreatorController
from use_cases import CampaignCreatorUseCase, CampaignListerUseCase
from repositories import CampaignRepository, RecipientRepository
from use_case_factories import QueueCreatorUseCaseFactory


class CampaignCreatorControllerFactory:
    @staticmethod
    def create(session) -> CampaignCreatorController:
        recipient_repo = RecipientRepository(session)
        campaign_repo = CampaignRepository(session, recipient_repo)
        queue_creator_use_case = QueueCreatorUseCaseFactory.create(session)
        campaign_creator_use_case = CampaignCreatorUseCase(
            campaign_repo, recipient_repo, queue_creator_use_case
        )
        return CampaignCreatorController(campaign_creator_use_case)


class CampaignListerControllerFactory:
    @staticmethod
    def create(session) -> CampaignListerController:
        recipient_repo = RecipientRepository(session)
        campaign_repo = CampaignRepository(session, recipient_repo)
        campaign_lister_use_case = CampaignListerUseCase(campaign_repo)
        return CampaignListerController(campaign_lister_use_case)
