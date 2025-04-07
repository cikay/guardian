from fastapi import APIRouter, Response

from controller_factories import (
    CampaignCreatorControllerFactory,
    CampaignListerControllerFactory,
)
from db_setup import SessionDep

from api_types import CampaignCreatorDTOAPI, CampaignReaderDTOAPI
from api_domain_mapper import CampaignAPIDomainMapper


campaign_router = APIRouter(prefix="/campaign")


@campaign_router.post("/")
def post_campaign(
    campaign: CampaignCreatorDTOAPI, session: SessionDep, response: Response
) -> CampaignReaderDTOAPI:

    campaign_domain = CampaignAPIDomainMapper.to_domain(campaign)
    controller = CampaignCreatorControllerFactory.create(session)

    data, code = controller.execute(campaign_domain)

    response.status_code = code
    return data


# @campaign_router.get("/")
# def list_campaign(session: SessionDep, response: Response) -> list[CampaignReaderDTOAPI]:

#     filter_set_domain = CampaignAPIDomainMapper.to_domain(filter_set)
#     controller = CampaignListerControllerFactory.create(session)
#     data, code = controller.execute(filter_set_domain)
#     response.status_code = code
#     return data
