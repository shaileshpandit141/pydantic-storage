from typing import Any, Literal

from pydantic import TypeAdapter, ValidationError
from pydantic.fields import FieldInfo

from pydantic_storage.types._generic_types import T


def check_model_kwargs(
    model: type[T],
    kwargs: dict[str, Any],
    mode: Literal["all", "partial"] = "partial",
) -> None:
    """
    Validate that kwargs match a Pydantic model's field names and types.

    mode="partial" -> only validate given keys
    mode="all"     -> require all model fields to be present in kwargs
    """
    field_list: dict[str, FieldInfo] = model.model_fields

    if mode == "all":
        missing = set(field_list.keys()) - set(kwargs.keys())
        if missing:
            raise ValidationError(f"Missing fields: {', '.join(missing)}")

    for key, value in kwargs.items():
        if key not in field_list:
            raise ValidationError(f"Field '{key}' is not a valid field of the model.")

        annotation = field_list[key].annotation
        try:
            TypeAdapter(annotation).validate_python(value)
        except Exception:
            raise ValidationError(
                f"Value for field '{key}' must be of type {annotation}, got {value!r}"
            )
