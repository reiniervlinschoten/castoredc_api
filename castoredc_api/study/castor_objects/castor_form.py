import itertools
from typing import List, Optional, Any, Union

from castoredc_api.study.castor_objects.castor_field import CastorField
from castoredc_api.study.castor_objects.castor_step import CastorStep


class CastorForm:
    """Object representing a form in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(
        self,
        form_collection_name: str,
        form_collection_id: str,
        form_collection_type: str,
        form_collection_order: str,
    ) -> None:
        """Creates a CastorForm."""
        self.form_name = form_collection_name
        self.form_id = form_collection_id
        self.form_type = form_collection_type
        self.form_order = int(form_collection_order)
        self.study = None
        self.steps_on_id = {}
        self.steps_on_name = {}

    def add_step(self, step: CastorStep) -> None:
        """Adds a CastorStep to the form."""
        self.steps_on_id[step.step_id] = step
        self.steps_on_name[step.step_name] = step
        step.form = self

    def get_all_steps(self) -> List[CastorStep]:
        """Returns a list of linked CastorSteps."""
        return list(self.steps_on_id.values())

    def get_single_step(self, step_id_or_name: str) -> Optional[CastorStep]:
        """Returns a linked CastorStep based on id or name."""
        step = self.steps_on_id.get(step_id_or_name)
        if step is None:
            return self.steps_on_name.get(step_id_or_name)
        else:
            return step

    def get_all_fields(self) -> List[CastorField]:
        """Returns a list of linked CastorFields."""
        return list(
            itertools.chain.from_iterable(
                [_step.get_all_fields() for _step in self.get_all_steps()]
            )
        )

    def get_single_field(self, field_id_or_name: str) -> Optional[CastorField]:
        """Returns a linked CastorField based on id or name."""
        for step in self.get_all_steps():
            # Search for field in each step
            field = step.get_single_field(field_id_or_name)
            # If field found (id and name are both unique)
            if field is not None:
                return field
        # If field not found
        return None

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorForm):
            return NotImplemented
        else:
            return self.form_id == other.form_id

    def __repr__(self) -> str:
        return self.form_name
