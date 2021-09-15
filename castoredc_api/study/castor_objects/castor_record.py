import itertools
from typing import Union, Any, TYPE_CHECKING, List, Optional, Dict

if TYPE_CHECKING:
    from castoredc_api.study.castor_objects.castor_form_instance import (
        CastorFormInstance,
    )
    from castoredc_api.study.castor_objects.castor_data_point import CastorDataPoint


class CastorRecord:
    """Object representing a Castor Record."""

    def __init__(self, record_id: str) -> None:
        """Creates a CastorRecord."""
        self.record_id = record_id
        self.institute = None
        self.randomisation_group = None
        self.randomisation_datetime = None
        self.study = None
        self.form_instances_ids = {}

    def add_form_instance(self, form_instance: "CastorFormInstance") -> None:
        """Adds a field to the record."""
        self.form_instances_ids[form_instance.instance_id] = form_instance
        form_instance.record = self

    def get_all_form_instances(self) -> List["CastorFormInstance"]:
        """Returns all form instances of the record"""
        return list(self.form_instances_ids.values())

    def get_single_form_instance_on_id(
        self, instance_id: str
    ) -> Optional["CastorFormInstance"]:
        """Returns a single form instance based on id. Returns None if form_instance not found."""
        return self.form_instances_ids.get(instance_id)

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the record"""
        data_points = list(
            itertools.chain.from_iterable(
                [
                    self.form_instances_ids[instance_id].get_all_data_points()
                    for instance_id in self.form_instances_ids
                ]
            )
        )
        return data_points

    def get_single_data_point(
        self, field_id_or_name: str, form_instance: str
    ) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id."""
        return self.get_single_form_instance_on_id(form_instance).get_single_data_point(
            field_id_or_name
        )

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorRecord):
            return NotImplemented
        else:
            return self.record_id == other.record_id

    def __repr__(self) -> str:
        return self.record_id
