import itertools
from typing import Union, Any, TYPE_CHECKING, List, Optional

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
        self.form_instances = []

    def add_form_instance(self, form_instance: "CastorFormInstance") -> None:
        """Adds a field to the record."""
        self.form_instances.append(form_instance)
        form_instance.record = self

    def get_all_form_instances(self) -> List["CastorFormInstance"]:
        """Returns all form instances of the record"""
        return self.form_instances

    def get_single_form_instance(
        self, instance_id: str
    ) -> Optional["CastorFormInstance"]:
        """Returns a single form instance based on id."""
        return next(
            (
                instance
                for instance in self.form_instances
                if instance.instance_id == instance_id
            ),
            None,
        )

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the record"""
        data_points = list(
            itertools.chain.from_iterable(
                [
                    _form_instance.get_all_data_points()
                    for _form_instance in self.form_instances
                ]
            )
        )
        return data_points

    def get_single_data_point(
        self, field_id_or_name: str, form_instance_id: str
    ) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id."""
        form_instance = self.get_single_form_instance(form_instance_id)
        return form_instance.get_single_data_point(field_id_or_name)

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorRecord):
            return NotImplemented
        else:
            return self.record_id == other.record_id

    def __repr__(self) -> str:
        return self.record_id
