from fastapi import APIRouter, Response

from controller_factories import (
    CreateCampaignControllerFactory,
    ListCampaignControllerFactory,
)
from db_setup import SessionDep

from api_types import CampaignCreateAPI, CampaignReadAPI


campaign_router = APIRouter(prefix="/campaign")


@campaign_router.post("/")
def post_campaign(campaign: CampaignCreateAPI, session: SessionDep, response: Response):
    controller = CreateCampaignControllerFactory.create(session)
    data, code = controller.execute(campaign.model_dump())

    response.status_code = code
    return data


@campaign_router.get("/")
def list_campaign(
    session: SessionDep,
    response: Response,
):
    controller = ListCampaignControllerFactory.create(session)
    data, code = controller.execute({})
    response.status_code = code
    return data
