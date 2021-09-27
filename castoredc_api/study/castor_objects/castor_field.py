"""Module for representing a CastorField in Python."""
from typing import Optional, Union, Any


class CastorField:
    """Object representing a Castor Field. Functions as a node of a tree for all interrelations."""

    # pylint: disable=too-many-instance-attributes
    # Field has more attributes

    def __init__(
        self,
        field_name: str,
        field_id: str,
        field_type: str,
        field_label: str,
        field_required: str,
        field_option_group: Optional[str],
        field_order: str,
    ) -> None:
        """Creates a CastorField."""
        self.field_id = field_id
        self.field_name = field_name
        self.field_label = field_label
        self.field_type = field_type
        self.field_required = bool(field_required == "1")
        self.field_option_group = field_option_group
        self.field_order = field_order
        self.step = None
        self.field_dependency = None
        self.field_max = None
        self.field_min = None

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorField):
            return NotImplemented
        return self.field_id == other.field_id

    def __repr__(self) -> str:
        return self.field_name
