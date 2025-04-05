from exceptions import CustomException

from use_cases import CampaignCreateUseCase, CampaignListUseCase
from dtos import CampaignFilterSet, CampaignCreate, CampaignRead
from dto_mapper import CampaignMapper


class CreateCampaignController:

    def __init__(self, use_case: CampaignCreateUseCase):
        self.use_case = use_case

    def execute(self, campaign_create: CampaignCreate) -> CampaignRead:
        try:
            entity = self.use_case.execute(campaign_create)
        except CustomException as e:
            return {"error": e.messages}, 400

        campaign_api_read = CampaignMapper.to_api(entity)

        return campaign_api_read, 201


class ListCampaignController:
    def __init__(self, use_case: CampaignListUseCase):
        self.use_case = use_case

    def execute(self, filter_set: CampaignFilterSet):
        try:
            entities = self.use_case.execute(filter_set)
        except CustomException as e:
            return {"error": str(e)}, 400

        campaign_api_read_entries = [
            CampaignMapper.to_api(entity) for entity in entities
        ]

        return campaign_api_read_entries, 200
