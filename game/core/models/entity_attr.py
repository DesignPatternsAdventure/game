"""Generic Entity Attributes."""

from pydantic import BaseModel


class EntityAttr(BaseModel):
    """Entity Attribute Model."""

    # TODO: Separate game units from pixels
    step_size: int | None = None
    """Optional step size in game units."""

    health: float | None = None
    """Optional current health."""

    counter: int | None = None
    """Optional count of uses or components."""

    # PLANNED: Consider other generic attributes to model
