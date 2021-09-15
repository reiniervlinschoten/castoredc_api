from typing import List, Any, Union, Optional
from castoredc_api.study.castor_objects.castor_field import CastorField


class CastorStep:
    """Object representing a step in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(self, step_name: str, step_id: str, step_order: str) -> None:
        """Creates a CastorStep object."""
        self.step_name = step_name
        self.step_id = step_id
        self.step_order = int(step_order)
        self.form = None
        self.fields_on_id = {}
        self.fields_on_name = {}

    def add_field(self, field: CastorField) -> None:
        """Adds a CastorField to the step."""
        self.fields_on_id[field.field_id] = field
        self.fields_on_name[field.field_name] = field
        field.step = self

    def get_all_fields(self) -> List[CastorField]:
        """Returns all linked CastorFields."""
        return list(self.fields_on_id.values())

    def get_single_field(self, field_id_or_name: str) -> Optional[CastorField]:
        """Returns a linked CastorField based on id or name."""
        field = self.fields_on_id.get(field_id_or_name)
        if field is None:
            return self.fields_on_name.get(field_id_or_name)
        else:
            return field

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorStep):
            return NotImplemented
        else:
            return self.step_id == other.step_id

    def __repr__(self) -> str:
        return self.step_name
