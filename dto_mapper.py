# api_mappers.py
from api_types import CampaignCreateAPI, CampaignReadAPI
from dtos import CampaignCreate, CampaignRead
from dataclasses import asdict


class CampaignMapper:
    @staticmethod
    def to_domain(campaign_api: CampaignCreateAPI) -> CampaignCreate:
        return CampaignCreate(**campaign_api.model_dump())

    @staticmethod
    def to_api(campaign_domain: CampaignRead) -> CampaignReadAPI:
        domain_dict = asdict(campaign_domain)
        return CampaignReadAPI(**domain_dict)
