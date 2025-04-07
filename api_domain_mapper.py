# api_mappers.py
from api_types import CampaignCreatorDTOAPI, CampaignReaderDTOAPI
from dtos import CampaignCreatorDTO, CampaignReaderDTO
from dataclasses import asdict


class CampaignAPIDomainMapper:
    @staticmethod
    def to_domain(campaign_api: CampaignCreatorDTOAPI) -> CampaignCreatorDTO:
        return CampaignCreatorDTO(**campaign_api.model_dump())

    @staticmethod
    def to_api(campaign_domain: CampaignReaderDTO) -> CampaignReaderDTOAPI:
        domain_dict = asdict(campaign_domain)
        return CampaignReaderDTOAPI(**domain_dict)
