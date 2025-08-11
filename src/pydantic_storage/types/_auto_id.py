from typing import Annotated

from pydantic import Field


class AutoIDMarker:
    """Marker type to identify AutoID fields."""

    pass


# Type alias with default built in
AutoID = Annotated[int, AutoIDMarker, Field(default=0, ge=0)]
