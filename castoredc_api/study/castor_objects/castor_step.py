from typing import List, Any, Union
from castoredc_api.study.castor_objects.castor_field import CastorField


class CastorStep:
    """Object representing a step in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(self, step_name: str, step_id: str, step_order: str) -> None:
        """Creates a CastorStep object."""
        self.step_name = step_name
        self.step_id = step_id
        self.step_order = int(step_order)
        self.form = None
        self.fields = []

    def add_field(self, field: CastorField) -> None:
        """Adds a CastorField to the step."""
        self.fields.append(field)
        field.step = self

    def get_all_fields(self) -> List[CastorField]:
        """Returns all linked CastorFields."""
        return self.fields

    def get_single_field(self, field_id_or_name: str) -> CastorField:
        """Returns a linked CastorField based on id or name."""
        return next(
            (
                field
                for field in self.fields
                if (
                    field.field_id == field_id_or_name
                    or field.field_name == field_id_or_name
                )
            ),
            None,
        )

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorStep):
            return NotImplemented
        else:
            return self.step_id == other.step_id

    def __repr__(self) -> str:
        return self.step_name
