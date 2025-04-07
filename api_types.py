from dtos import CampaignCreatorDTO, CampaignReaderDTO
from type_conversion import create_api_type

create_type_exclude_fields = {"created_at", "updated_at"}
type_registry = {}

CampaignCreatorDTOAPI = create_api_type(
    CampaignCreatorDTO,
    "CampaignCreatorDTOAPI",
    type_registry,
    create_type_exclude_fields,
)
CampaignReaderDTOAPI = create_api_type(
    CampaignReaderDTO, "CampaignReaderDTOAPI", type_registry
)
