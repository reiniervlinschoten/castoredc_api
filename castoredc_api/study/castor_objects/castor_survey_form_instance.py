from typing import TYPE_CHECKING, Union

from castoredc_api import CastorException
from castoredc_api.study.castor_objects.castor_form_instance import CastorFormInstance

if TYPE_CHECKING:
    from castoredc_api.study.castor_study import CastorStudy


class CastorSurveyFormInstance(CastorFormInstance):
    """Object representing a Castor survey form instance."""

    def __init__(
        self,
        instance_id: str,
        name_of_form: str,
        study: "CastorStudy",
    ) -> None:
        """Creates a CastorSurveyFormInstance."""
        super().__init__(instance_id, name_of_form, study, "Survey")

        # Relevant survey data
        self.created_on = None
        self.parent = None
        self.archived = None
        self.sent_on = None
        self.progress = None
        self.completed_on = None
        self.survey_package_id = None

    # Helpers
    def find_form(self, study: "CastorStudy") -> Union["CastorForm", CastorException]:
        """Find which form is the originator of this instance."""
        # Surveys can be found on name_of_form
        return study.instance_of_form(self.name_of_form, self.instance_type)
