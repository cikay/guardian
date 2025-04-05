from dataclasses import fields
from dtos import ComparisonOperatorSet, UNSET
from typing import Protocol


class OrmOperatorSetProtocol(Protocol):
    def eq(self, field: str, value): ...

    def ne(self, field: str, value): ...

    def gt(self, field: str, value): ...

    def gte(self, field: str, value): ...

    def lt(self, field: str, value): ...

    def lte(self, field: str, value): ...

    def in_(self, field: str, value): ...


class FilterConverter:

    def __init__(self, orm_operator_set: OrmOperatorSetProtocol):
        self.orm_operator_set = orm_operator_set

    def convert(self, filter_set) -> list:
        orm_filter_set = []

        for field in fields(filter_set):
            field_name = field.name
            value = getattr(filter_set, field_name)

            if value is UNSET:
                continue

            if isinstance(value, ComparisonOperatorSet):
                orm_filter_set.extend(self._convert_field_filters(field_name, value))
            else:
                func = getattr(self.orm_operator_set, "eq")

                orm_filter_set.append(func(field_name, value))

        return orm_filter_set

    def _convert_field_filters(self, field: str, operator_set: ComparisonOperatorSet):
        filters = []

        for operator in fields(operator_set):
            operator_name = operator.name
            value = getattr(operator_set, operator_name)

            if value is UNSET:
                continue

            func = getattr(self.orm_operator_set, operator_name, None)
            if not func:
                raise ValueError(f"Unsupported operator: {operator_name}")

            filter = func(field, value)
            filters.append(filter)

        return filters


class SqlAlchemyOperatorSet(OrmOperatorSetProtocol):
    def __init__(self, model):
        self.model = model

    def eq(self, field, value):
        field = getattr(self.model, field)
        return field == value

    def ne(self, field, value):
        field = getattr(self.model, field)
        return field != value

    def gt(self, field, value):
        field = getattr(self.model, field)

        return field > value

    def gte(self, field, value):
        field = getattr(self.model, field)

        return field >= value

    def lt(self, field, value):
        field = getattr(self.model, field)

        return field < value

    def lte(self, field, value):
        field = getattr(self.model, field)

        return field <= value

    def in_(self, field, value):
        field = getattr(self.model, field)

        return field.in_(value)
