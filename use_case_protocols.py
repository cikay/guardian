from typing import Protocol

from entities import CampaignEntity
from dtos import CampaignCreatorDTO, CampaignFilterSet


class CampaignCreatorUseCaseProtocol(Protocol):

    def execute(self, campaign_creator: CampaignCreatorDTO) -> CampaignEntity: ...


class CampaignListerUseCaseProtocol(Protocol):

    def execute(
        self, campaign_filter_set: CampaignFilterSet
    ) -> list[CampaignEntity]: ...
