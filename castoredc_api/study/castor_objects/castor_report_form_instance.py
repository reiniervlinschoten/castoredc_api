from typing import TYPE_CHECKING
from castoredc_api.study.castor_objects.castor_form_instance import CastorFormInstance

if TYPE_CHECKING:
    from castoredc_api.study.castor_study import CastorStudy


class CastorReportFormInstance(CastorFormInstance):
    """Object representing a Castor report form instance."""

    def __init__(
        self,
        instance_id: str,
        name_of_form: str,
        study: "CastorStudy",
    ) -> None:
        """Creates a CastorFormInstance."""
        super().__init__(instance_id, name_of_form, study, "Report")
