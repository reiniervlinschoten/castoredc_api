from datetime import datetime
from typing import Union, Any, TYPE_CHECKING, List
from castoredc_api import CastorException

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from castoredc_api.study.castor_objects.castor_field import CastorField
    from castoredc_api.study.castor_study import CastorStudy


class CastorDataPoint:
    """Object representing a Castor datapoint. Is an instance of a field with a value for a record.."""

    def __init__(
        self,
        field_id: str,
        raw_value: Union[str, int],
        study: "CastorStudy",
        filled_in: str,
    ) -> None:
        """Creates a CastorField."""
        self.field_id = field_id
        self.raw_value = raw_value
        self.instance_of = self.find_field(study)
        if self.instance_of is None:
            raise CastorException(
                "The field that this is an instance of does not exist in the study!"
            )
        self.form_instance = None
        self.filled_in = (
            None
            if filled_in == ""
            else datetime.strptime(filled_in, "%Y-%m-%d %H:%M:%S")
        )
        # Is missing
        self.value = self.__interpret(study)

    # Helpers
    def find_field(self, study: "CastorStudy") -> "CastorField":
        return study.get_single_field(self.field_id)

    def __interpret(self, study: "CastorStudy"):
        """Transform the raw value into analysable data."""
        if self.instance_of.field_type in ["checkbox", "dropdown", "radio"]:
            return self.__interpret_optiongroup(study)
        elif self.instance_of.field_type in [
            "numeric",
            "year",
            "slider",
            "randomization",
        ]:
            return self.__interpret_numeric()
        elif self.instance_of.field_type in ["string", "textarea", "upload"]:
            return self.raw_value
        elif self.instance_of.field_type in ["calculation"]:
            try:
                return self.__interpret_numeric()
            except ValueError:
                return self.raw_value
        elif self.instance_of.field_type in ["date", "datetime"]:
            return self.__interpret_datetime()
        elif self.instance_of.field_type in ["time"]:
            return self.__interpret_time()
        elif self.instance_of.field_type in ["numberdate"]:
            return self.__interpret_numberdate()
        else:
            return "Error"

    def __interpret_time(self):
        """Interprets time missing data while handling user missings."""
        if self.raw_value == "":
            return np.datetime64("NaT")
        elif "Missing" in self.raw_value:
            if "measurement failed" in self.raw_value:
                return -95
            elif "not applicable" in self.raw_value:
                return -96
            elif "not asked" in self.raw_value:
                return -97
            elif "asked but unknown" in self.raw_value:
                return -98
            elif "not done" in self.raw_value:
                return -99
        else:
            return datetime.strptime(self.raw_value, "%H:%M").time()

    def __interpret_datetime(self):
        """Interprets date and datetime data while handling user missings."""
        if self.raw_value == "":
            return np.nan
        elif "Missing" in self.raw_value:
            if "measurement failed" in self.raw_value:
                return pd.Period(year=2995, month=1, day=1, freq="D").strftime(
                    "%d-%m-%Y"
                )
            elif "not applicable" in self.raw_value:
                return pd.Period(year=2996, month=1, day=1, freq="D").strftime(
                    "%d-%m-%Y"
                )
            elif "not asked" in self.raw_value:
                return pd.Period(year=2997, month=1, day=1, freq="D").strftime(
                    "%d-%m-%Y"
                )
            elif "asked but unknown" in self.raw_value:
                return pd.Period(year=2998, month=1, day=1, freq="D").strftime(
                    "%d-%m-%Y"
                )
            elif "not done" in self.raw_value:
                return pd.Period(year=2999, month=1, day=1, freq="D").strftime(
                    "%d-%m-%Y"
                )

        elif self.instance_of.field_type == "date":
            return pd.Period(
                datetime.strptime(self.raw_value, "%d-%m-%Y"), freq="D"
            ).strftime("%d-%m-%Y")

        elif self.instance_of.field_type == "datetime":
            return pd.Period(
                datetime.strptime(self.raw_value, "%d-%m-%Y;%H:%M"), freq="S"
            ).strftime("%d-%m-%Y %H:%M:%S")

    def __interpret_optiongroup(self, study: "CastorStudy"):
        """Interprets optiongroup data while handling user missings."""
        if self.raw_value == "":
            return ""
        elif "Missing" in self.raw_value:
            if "measurement failed" in self.raw_value:
                return "measurement failed"
            elif "not applicable" in self.raw_value:
                return "not applicable"
            elif "not asked" in self.raw_value:
                return "not asked"
            elif "asked but unknown" in self.raw_value:
                return "asked but unknown"
            elif "not done" in self.raw_value:
                return "not done"
        else:
            # Get the optiongroup for this data point
            optiongroup = self.instance_of.field_option_group
            # Retrieve the options
            study_optiongroup = study.get_single_optiongroup(optiongroup)
            if study_optiongroup is None:
                raise CastorException(
                    "Optiongroup not found. Is id correct and are optiongroups loaded?"
                )
            # Get options
            options = study_optiongroup["options"]
            # Transform options into dict value: name
            link = {item["value"]: item["name"] for item in options}
            # Get values, split by ; for checklists
            value_list = self.raw_value.split(";")
            # Values to names
            if value_list == [""]:
                new_values = [""]
            else:
                new_values = [link[value] for value in value_list]
            # Return a string, for multiple answers separate them with |
            return "|".join(new_values)

    def __interpret_numeric(self):
        """Interprets numeric data while handling user missings."""
        if self.raw_value == "":
            return np.nan
        elif "Missing" in self.raw_value:
            if "measurement failed" in self.raw_value:
                return -95
            elif "not applicable" in self.raw_value:
                return -96
            elif "not asked" in self.raw_value:
                return -97
            elif "asked but unknown" in self.raw_value:
                return -98
            elif "not done" in self.raw_value:
                return -99
        else:
            return float(self.raw_value)

    def __interpret_numberdate(self):
        """Interprets numberdate data while handling user missings."""
        if "Missing" in self.raw_value:
            if "measurement failed" in self.raw_value:
                return [-95, "01-01-2995"]
            elif "not applicable" in self.raw_value:
                return [-96, "01-01-2996"]
            elif "not asked" in self.raw_value:
                return [-97, "01-01-2997"]
            elif "asked but unknown" in self.raw_value:
                return [-98, "01-01-2998"]
            elif "not done" in self.raw_value:
                return [-99, "01-01-2999"]
        else:
            # Get number and date from the string
            number, date = self.raw_value.split(";")
            # Combine
            if number == "":
                number = np.nan
            if date == "":
                date = np.nan
            return [float(number), date]

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorDataPoint):
            return NotImplemented
        else:
            return (
                (self.field_id == other.field_id)
                and (self.form_instance == other.form_instance)
                and (self.form_instance.record == other.form_instance.record)
            )

    def __repr__(self) -> str:
        return (
            self.form_instance.record.record_id
            + " - "
            + self.form_instance.instance_of.form_name
            + " - "
            + self.instance_of.field_name
        )
