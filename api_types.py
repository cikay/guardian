from dtos import CampaignCreate, CampaignRead
from type_conversion import create_api_type

create_type_exclude_fields = {"created_at", "updated_at"}
type_registry = {}


CampaignCreateAPI = create_api_type(
    CampaignCreate,
    "CampaignCreateAPI",
    type_registry,
    create_type_exclude_fields,
)
CampaignReadAPI = create_api_type(CampaignRead, "CampaignReadAPI", type_registry)
