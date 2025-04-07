from exceptions import CustomException

from use_case_protocols import (
    CampaignCreatorUseCaseProtocol,
    CampaignListerUseCaseProtocol,
)
from dtos import CampaignFilterSet, CampaignCreatorDTO, CampaignReaderDTO
from api_domain_mapper import CampaignAPIDomainMapper


class CampaignCreatorController:

    def __init__(self, use_case: CampaignCreatorUseCaseProtocol):
        self.use_case = use_case

    def execute(self, campaign_creator: CampaignCreatorDTO) -> CampaignReaderDTO:
        try:
            entity = self.use_case.execute(campaign_creator)
        except CustomException as e:
            return {"error": e.messages}, 400

        campaign_api_read = CampaignAPIDomainMapper.to_api(entity)

        return campaign_api_read, 201


class CampaignListerController:

    def __init__(self, use_case: CampaignListerUseCaseProtocol):
        self.use_case = use_case

    def execute(self, filter_set: CampaignFilterSet):
        try:
            entities = self.use_case.execute(filter_set)
        except CustomException as e:
            return {"error": str(e)}, 400

        campaign_api_read_entries = [
            CampaignAPIDomainMapper.to_api(entity) for entity in entities
        ]

        return campaign_api_read_entries, 200
