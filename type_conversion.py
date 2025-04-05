from typing import get_type_hints, get_args, get_origin, Union, ForwardRef
from pydantic import create_model


def resolve_forward_ref(type_, globalns):
    if isinstance(type_, ForwardRef):
        return eval(type_.__forward_arg__, globalns)
    return type_


def ensure_api_type(type_, type_registry, globalns):
    resolved = resolve_forward_ref(type_, globalns)

    if resolved in type_registry:
        return type_registry[resolved]

    # If it's a user-defined class with annotations (likely a dataclass)
    if hasattr(resolved, "__annotations__"):
        return create_api_type(resolved, f"{resolved.__name__}API", type_registry)

    # Primitive or unhandled type (str, int, etc.)
    return resolved


def create_api_type(entity_type, type_name, type_registry, exclude_fields=None):
    if entity_type in type_registry:
        return type_registry[entity_type]

    exclude_fields = exclude_fields or set()
    globalns = vars(__import__(entity_type.__module__))

    hints = get_type_hints(entity_type, globalns=globalns)
    api_hints = {}

    for key, value in hints.items():
        if key in exclude_fields:
            continue

        origin = get_origin(value)
        args = get_args(value)

        if origin is list and args:
            inner_type = ensure_api_type(args[0], type_registry, globalns)
            api_hints[key] = (list[inner_type], ...)
        elif origin is Union and args:
            mapped_args = tuple(
                ensure_api_type(arg, type_registry, globalns) for arg in args
            )
            api_hints[key] = (Union[mapped_args], ...)
        else:
            final_type = ensure_api_type(value, type_registry, globalns)
            api_hints[key] = (final_type, ...)

    model = create_model(type_name, **api_hints)
    model.model_rebuild()
    type_registry[entity_type] = model
    return model
