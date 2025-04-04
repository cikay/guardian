from dataclasses import asdict

from exceptions import CustomException

from use_cases import CampaignCreateUseCase, CampaignListUseCase
from dtos import CampaignRead, CampaignCreate, CampaignQuery


class CreateCampaignController:

    def __init__(self, use_case: CampaignCreateUseCase):
        self.use_case = use_case

    def execute(self, campaign: dict) -> CampaignRead:
        campaign = CampaignCreate(**campaign)
        try:
            campaign_entity = self.use_case.execute(campaign)
        except CustomException as e:
            return {"error": e.messages}, 400

        campaign_api_read = CampaignRead(**asdict(campaign_entity))

        return campaign_api_read, 201


class ListCampaignController:
    def __init__(self, use_case: CampaignListUseCase):
        self.use_case = use_case

    def execute(self, query: dict):
        query = CampaignQuery(**query)
        try:
            campaign_entity = self.use_case.execute(query)
        except CustomException as e:
            return {"error": str(e)}, 400


        return campaign_entity, 200
