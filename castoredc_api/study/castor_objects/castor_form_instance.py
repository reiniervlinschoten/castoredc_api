from typing import Union, Any, TYPE_CHECKING, List, Optional
from castoredc_api import CastorException

if TYPE_CHECKING:
    from castoredc_api.study.castor_objects.castor_data_point import CastorDataPoint
    from castoredc_api.study.castor_objects.castor_form import CastorForm
    from castoredc_api.study.castor_study import CastorStudy


class CastorFormInstance:
    """Object representing a Castor form instance. Examples are survey instance or report instance."""

    def __init__(
        self,
        instance_id: str,
        name_of_form: str,
        study: "CastorStudy",
        instance_type: str,
    ) -> None:
        """Creates a CastorFormInstance."""
        self.instance_id = instance_id
        self.name_of_form = name_of_form
        self.instance_type = instance_type
        self.record = None
        self.data_points_on_id = {}
        self.data_points_on_name = {}

        self.instance_of = self.find_form(study)
        if self.instance_of is None:
            raise CastorException(
                f"{self.instance_type} {self.name_of_form} {self.instance_id} "
                f"- The form that this is an instance of does not exist in the study!"
            )

    def add_data_point(self, data_point: "CastorDataPoint") -> None:
        """Adds a data point to the form instance."""
        self.data_points_on_id[data_point.field_id] = data_point
        self.data_points_on_name[data_point.instance_of.field_name] = data_point
        data_point.form_instance = self

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the form instance"""
        return list(self.data_points_on_id.values())

    def get_single_data_point(
        self, field_id_or_name: str
    ) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id or name. Returns None if not found on id or name."""
        data_point = self.data_points_on_id.get(field_id_or_name)
        if data_point is None:
            return self.data_points_on_name.get(field_id_or_name)
        else:
            return data_point

    # Helpers
    def find_form(self, study: "CastorStudy") -> Union["CastorForm", CastorException]:
        """Find which form is the originator of this instance."""
        # Reports and Study can be found on instance_id. Survey has its own version.
        return study.instance_of_form(self.instance_id, self.instance_type)

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorFormInstance):
            return NotImplemented
        else:
            return (
                self.instance_id == other.instance_id
                and self.instance_type == other.instance_type
                and self.record == other.record
            )

    def __repr__(self) -> str:
        return self.record.record_id + " - " + self.instance_of.form_name
