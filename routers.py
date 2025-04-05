from fastapi import APIRouter, Response

from controller_factories import (
    CreateCampaignControllerFactory,
    ListCampaignControllerFactory,
)
from db_setup import SessionDep

from api_types import CampaignCreateAPI, CampaignReadAPI
from dto_mapper import CampaignMapper


campaign_router = APIRouter(prefix="/campaign")


@campaign_router.post("/")
def post_campaign(
    campaign: CampaignCreateAPI, session: SessionDep, response: Response
) -> CampaignReadAPI:

    campaign_domain = CampaignMapper.to_domain(campaign)
    controller = CreateCampaignControllerFactory.create(session)

    data, code = controller.execute(campaign_domain)

    response.status_code = code
    return data


# @campaign_router.get("/")
# def list_campaign(session: SessionDep, response: Response) -> list[CampaignReadAPI]:

#     filter_set_domain = CampaignMapper.to_domain(filter_set)
#     controller = ListCampaignControllerFactory.create(session)
#     data, code = controller.execute(filter_set_domain)
#     response.status_code = code
#     return data
