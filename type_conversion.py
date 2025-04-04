from typing import get_type_hints

from pydantic import create_model


def create_api_type(entity_type, type_name, exclude_fields=None):
    exclude_fields = exclude_fields or set()
    hints = get_type_hints(entity_type)

    api_hints = {
        key: (value, ...) for key, value in hints.items() if key not in exclude_fields
    }

    return create_model(type_name, **api_hints)
