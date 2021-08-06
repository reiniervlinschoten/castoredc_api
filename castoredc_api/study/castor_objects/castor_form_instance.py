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
        instance_type: str,
        name_of_form: str,
        study: "CastorStudy",
    ) -> None:
        """Creates a CastorFormInstance."""
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.name_of_form = name_of_form
        self.record = None

        self.instance_of = self.find_form(study)
        if self.instance_of is None:
            raise CastorException(
                f"{instance_type} {name_of_form} {instance_id} "
                f"- The form that this is an instance of does not exist in the study!"
            )

        self.data_points = []

        # Relevant survey data
        # TODO: probably better to refactor and make special class survey_form that inherits from this class
        self.created_on = None  # Also for report
        self.parent = None  # Also for report, TODO: not retrieved from API for survey_package_instance?
        self.archived = None
        self.sent_on = None
        self.progress = None
        self.completed_on = None
        self.survey_package_id = None

    def add_data_point(self, data_point: "CastorDataPoint") -> None:
        """Adds a data point to the form instance."""
        self.data_points.append(data_point)
        data_point.form_instance = self

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the form instance"""
        return self.data_points

    def get_single_data_point(
        self, field_id_or_name: str
    ) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id or name."""
        return next(
            (
                data_point
                for data_point in self.data_points
                if (
                    data_point.field_id == field_id_or_name
                    or data_point.instance_of.field_name == field_id_or_name
                )
            ),
            None,
        )

    # Helpers
    def find_form(self, study: "CastorStudy") -> Union["CastorForm", CastorException]:
        """Find which form is the originator of this instance."""
        if self.instance_type == "Survey":
            # Surveys can be found on name_of_form
            return study.instance_of_form(self.name_of_form, self.instance_type)
        else:
            # Reports can be found on instance_id
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
