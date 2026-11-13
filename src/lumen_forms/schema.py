"""Form schema model for Lumen Forms."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


Validator = Callable[[Any], Any]


@dataclass
class Field:
    name: str
    kind: str = "text"
    required: bool = False
    validators: List[Validator] = field(default_factory=list)


@dataclass
class Schema:
    fields: List[Field]

    def validate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        errors: Dict[str, str] = {}
        for item in self.fields:
            value = payload.get(item.name)
            if item.required and value in (None, ""):
                errors[item.name] = "required"
                continue
            for validator in item.validators:
                try:
                    validator(value)
                except ValueError as exc:
                    errors[item.name] = str(exc)
                    break
        return errors
