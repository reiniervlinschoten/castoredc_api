"""Module for representing a CastorStudy in Python."""
import itertools
import math
import pathlib
import re
import sys
from datetime import datetime
from operator import attrgetter
from typing import List, Optional, Any, Union, Dict

import pandas as pd
from tqdm import tqdm

from castoredc_api import CastorClient, CastorException
from castoredc_api.study.castor_objects.castor_data_point import CastorDataPoint
from castoredc_api.study.castor_objects import (
    CastorField,
    CastorFormInstance,
    CastorRecord,
    CastorStep,
    CastorForm,
    CastorStudyFormInstance,
    CastorSurveyFormInstance,
    CastorReportFormInstance,
)


class CastorStudy:
    """Object representing a study in Castor.
    Functions as the head of a tree for all interrelations.
    Needs an authenticated api_client that is linked to the same study_id to call data."""

    # pylint: disable=too-many-instance-attributes
    # Necessary number of attributes to allow caching of information
    # pylint: disable=too-many-public-methods
    # Necessary number of public methods to interact with study
    # pylint: disable=too-many-arguments
    # Necessary number of arguments to setup study
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        study_id: str,
        url: str,
        test=False,
        format_options=None,
    ) -> None:
        """Create a CastorStudy object."""
        self.study_id = study_id
        # Set configuration settings
        self.configuration = {
            "date": "%d-%m-%Y",
            "datetime": "%d-%m-%Y %H:%M",
            "datetime_seconds": "%d-%m-%Y %H:%M:%S",
            "time": "%H:%M",
        }
        if format_options:
            self.configuration.update(format_options)
        # Create the client to interact with the study
        if test is False:
            self.client = CastorClient(client_id, client_secret, url)
            self.client.link_study(study_id)
        # List of all forms in the study - structure
        self.forms_on_id = {}
        self.forms_on_name = {}
        # Dictionary to store the relationship between a form instance and its form ID
        self.form_links = {}
        # List of all records in the study - data
        self.records = {}
        # List of dictionaries of optiongroups
        self.optiongroups = {}
        # Container variables to save time querying the database
        self.__all_report_instances = {}

    # STRUCTURE MAPPING
    def map_structure(self) -> None:
        """Maps the structure for the study."""
        # Reset structure & data
        self.forms_on_id = {}
        self.forms_on_name = {}
        self.form_links = {}
        self.records = {}
        self.optiongroups = {}
        self.__all_report_instances = {}
        # Get the structure from the API
        print("Downloading Study Structure.", flush=True, file=sys.stderr)
        data = self.client.export_study_structure()
        # Loop over all fields
        for field in tqdm(data, desc="Mapping Study Structure"):
            # Check if the form for the field exists, if not, create it
            form = self.get_single_form(field["Form Collection ID"])
            if form is None:
                form = CastorForm(
                    form_collection_type=field["Form Type"],
                    form_collection_id=field["Form Collection ID"],
                    form_collection_name=field["Form Collection Name"],
                    form_collection_order=field["Form Collection Order"],
                )
                self.add_form(form)
            # Check if the step for the field exists, if not, create it
            step = form.get_single_step(field["Form ID"])
            if step is None:
                step = CastorStep(
                    step_id=field["Form ID"],
                    step_name=field["Form Name"],
                    step_order=field["Form Order"],
                )
                form.add_step(step)
            # Create the field
            new_field = CastorField(
                field_id=field["Field ID"],
                field_name=field["Field Variable Name"],
                field_label=field["Field Label"],
                field_type=field["Field Type"],
                field_required=field["Field Required"],
                field_option_group=field["Field Option Group"],
                field_order=field["Field Order"],
            )
            step.add_field(new_field)
        # Augment field data
        self.__load_field_information()

        # Map the field dependencies and optiongroups
        self.__map_field_dependencies()
        self.__load_optiongroups()

    # DATA MAPPING
    def map_data(self) -> None:
        """Maps the data for the study."""
        self.map_structure()
        self.update_links()
        self.__link_data()
        self.__load_record_information()
        self.__load_survey_information()
        self.__load_report_information()

    def update_links(self) -> None:
        """Creates the links between form and form instances."""
        # Reset form links
        self.form_links = {}
        # Get the name of the survey forms, as the export data can only be linked on name, not on id
        print("Downloading Surveys.", flush=True, file=sys.stderr)
        surveys = self.client.all_surveys()
        self.form_links["Survey"] = {survey["name"]: survey["id"] for survey in surveys}
        # Get all report instances that need to be linked
        print("Downloading Report Instances.", flush=True, file=sys.stderr)
        # Save this data from the database to save time later
        report_instances = self.client.all_report_instances(archived=0)
        archived_report_instances = self.client.all_report_instances(archived=1)
        # Create dict with link id: object
        self.__all_report_instances = {
            report_instance["id"]: report_instance
            for report_instance in report_instances + archived_report_instances
        }
        # Create dict with link instance_id: form_id
        self.form_links["Report"] = {
            instance_id: self.__all_report_instances[instance_id]["_embedded"][
                "report"
            ]["id"]
            for instance_id in self.__all_report_instances
        }

    # OPTIONGROUPS
    def __load_optiongroups(self) -> None:
        """Loads all optiongroups through the client"""
        # Get the optiongroups
        print("Downloading Optiongroups", flush=True, file=sys.stderr)
        optiongroups = self.client.all_field_optiongroups()
        self.optiongroups = {
            optiongroup["id"]: optiongroup for optiongroup in optiongroups
        }

    # AUXILIARY DATA
    def __load_record_information(self) -> None:
        """Adds auxiliary data to records."""
        print("Downloading Record Information.", flush=True, file=sys.stderr)
        record_data = self.client.all_records()
        for record_api in tqdm(record_data, desc="Augmenting Record Data"):
            record = self.get_single_record(record_api["id"])
            record.institute = record_api["_embedded"]["institute"]["name"]
            record.randomisation_group = record_api["randomization_group_name"]
            record.randomisation_datetime = self.__get_date_or_none(
                record_api["randomized_on"]
            )
            record.archived = record_api["archived"]

    def __load_survey_information(self) -> None:
        """Adds auxiliary data to survey forms."""
        print("Downloading Survey Information.", flush=True, file=sys.stderr)
        survey_package_data = self.client.all_survey_package_instances()
        # Create mapping {survey_instance_id: survey_package}
        survey_data = {
            survey["id"]: {
                "package": package,
                "record": package["record_id"],
                "survey": survey,
            }
            for package in survey_package_data
            for survey in package["_embedded"]["survey_instances"]
        }
        for survey_instance, values in tqdm(
            survey_data.items(), desc="Augmenting Survey Data"
        ):
            # Test if instance in study
            local_instance = self.get_single_form_instance_on_id(
                instance_id=survey_instance, record_id=values["record"]
            )
            local_instance.created_on = self.__get_date_or_none(
                values["package"]["created_on"]
            )
            local_instance.sent_on = self.__get_date_or_none(
                values["package"]["sent_on"]
            )
            local_instance.progress = values["survey"]["progress"]
            local_instance.completed_on = self.__get_date_or_none(
                values["package"]["finished_on"]
            )
            local_instance.archived = values["package"]["archived"]
            local_instance.survey_package_id = values["package"]["id"]
            local_instance.survey_package_name = values["package"][
                "survey_package_name"
            ]

    def __load_report_information(self) -> None:
        """Adds auxiliary data to report forms."""
        for instance_id, report_instance in tqdm(
            self.__all_report_instances.items(),
            "Augmenting Report Data",
        ):
            # Test if instance in study
            local_instance = self.get_single_form_instance_on_id(
                instance_id=instance_id, record_id=report_instance["record_id"]
            )
            local_instance.created_on = datetime.strptime(
                report_instance["created_on"], "%Y-%m-%d %H:%M:%S"
            ).strftime(self.configuration["datetime_seconds"])
            if report_instance["parent_type"] == "phase":
                local_instance.parent = self.get_single_form(
                    report_instance["parent_id"]
                ).form_name
            elif report_instance["parent_type"] == "reportInstance":
                local_instance.parent = self.get_single_form_instance_on_id(
                    report_instance["record_id"], report_instance["parent_id"]
                ).name_of_form
            else:
                local_instance.parent = "No parent"
            local_instance.archived = report_instance["archived"]

    def __load_field_information(self):
        """Adds auxillary information to fields."""
        all_fields = self.client.all_fields()
        for api_field in all_fields:
            field = self.get_single_field(api_field["id"])
            # Use -inf and inf for easy numeric comparison
            field.field_min = (
                -math.inf if api_field["field_min"] is None else api_field["field_min"]
            )
            field.field_max = (
                math.inf if api_field["field_max"] is None else api_field["field_max"]
            )

    def __get_date_or_none(self, dictionary: Optional[dict]) -> Optional[datetime]:
        """Returns the date or None when no date found."""
        date = (
            None
            if dictionary is None
            else datetime.strptime(dictionary["date"], "%Y-%m-%d %H:%M:%S.%f").strftime(
                self.configuration["datetime_seconds"]
            )
        )
        return date

    # FIELD DEPENDENCIES
    def __map_field_dependencies(self) -> None:
        """Retrieves all field_dependencies and links them to the right field."""
        print("Downloading Field Dependencies", flush=True, file=sys.stderr)
        dependencies = self.client.all_field_dependencies()
        # Format to dict of {child_id: {"parent_field": parent_field, "parent_value": value}
        dependencies = {
            dep["child_id"]: {
                "parent_field": self.get_single_field(dep["parent_id"]),
                "parent_value": dep["value"],
            }
            for dep in dependencies
        }
        for child_id in dependencies:
            self.get_single_field(child_id).field_dependency = dependencies[child_id]

    # DATA ANALYSIS
    def export_to_dataframe(self, archived=False) -> dict:
        """Exports all data from a study into a dict of dataframes for statistical analysis."""
        self.map_data()
        dataframes = {
            "Study": self.__export_study_data(archived),
            "Surveys": self.__export_survey_data(archived),
            "Reports": self.__export_report_data(archived),
        }
        return dataframes

    def export_to_csv(self, archived=False) -> dict:
        """Exports all data to csv files.
        Returns dict with file locations."""
        now = f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')[:-3]}"
        dataframes = self.export_to_dataframe(archived)
        # Instantiate output folder
        pathlib.Path(pathlib.Path.cwd(), "output").mkdir(parents=True, exist_ok=True)
        # Export dataframes
        dataframes["Study"] = self.export_dataframe_to_csv(
            dataframes["Study"], "Study", now
        )
        for survey in dataframes["Surveys"]:
            dataframes["Surveys"][survey] = self.export_dataframe_to_csv(
                dataframes["Surveys"][survey], survey, now
            )
        for report in dataframes["Reports"]:
            dataframes["Reports"][report] = self.export_dataframe_to_csv(
                dataframes["Reports"][report], report, now
            )
        return dataframes

    def export_to_feather(self, archived=False) -> dict:
        """Exports all data to feather files.
        Returns dict of file locations for export into R."""
        now = f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')[:-3]}"
        dataframes = self.export_to_dataframe(archived)
        # Instantiate output folder
        pathlib.Path(pathlib.Path.cwd(), "output").mkdir(parents=True, exist_ok=True)
        print("Writing data to feather files...", flush=True, file=sys.stderr)
        dataframes["Study"] = self.export_dataframe_to_feather(
            dataframes["Study"], "Study", now
        )
        for report in dataframes["Reports"]:
            dataframes["Reports"][report] = self.export_dataframe_to_feather(
                dataframes["Reports"][report], report, now
            )
        for survey in dataframes["Surveys"]:
            dataframes["Surveys"][survey] = self.export_dataframe_to_feather(
                dataframes["Surveys"][survey], survey, now
            )
        return dataframes

    def export_dataframe_to_csv(
        self, dataframe: pd.DataFrame, name: str, now: str
    ) -> str:
        """Exports a single dataframe to csv and returns the destination path."""
        filename = re.sub(r"[^\w\-_\. ]", "_", name)
        path = pathlib.Path(
            pathlib.Path.cwd(), "output", f"{now} {self.study_id} {filename}.csv"
        )
        dataframe.to_csv(
            path_or_buf=path,
            sep=";",
            index=False,
        )
        return str(path)

    def export_dataframe_to_feather(
        self, dataframe: pd.DataFrame, name: str, now: str
    ) -> str:
        """Exports a single dataframe to feather and returns the destination path."""
        filename = re.sub(r"[^\w\-_\. ]", "_", name)

        path = pathlib.Path(
            pathlib.Path.cwd(), "output", f"{now} {self.study_id} {filename}.feather"
        )
        if dataframe.empty:
            # If dataframe is empty, set all dtypes to object
            # See also https://github.com/reiniervlinschoten/castoredc_api/issues/44
            dataframe = dataframe.astype("object")

        dataframe.reset_index(drop=True).to_feather(
            path,
            compression="uncompressed",
        )
        return str(path)

    # HELPERS
    def get_single_optiongroup(self, optiongroup_id: str) -> Optional[Dict]:
        """Get a single optiongroup based on id."""
        return self.optiongroups.get(optiongroup_id)

    def add_form(self, form: CastorForm) -> None:
        """Add a CastorForm to the study."""
        self.forms_on_id[form.form_id] = form
        self.forms_on_name[form.form_name] = form
        form.study = self

    def get_all_forms(self) -> List[CastorForm]:
        """Get all linked CastorForms."""
        return list(self.forms_on_id.values())

    def get_all_survey_forms(self) -> List[CastorForm]:
        """Gets all survey CastorForms."""
        return self.get_all_form_type_forms("Survey")

    def get_all_report_forms(self) -> List[CastorForm]:
        """Gets all report CastorForms."""
        return self.get_all_form_type_forms("Report")

    def get_all_form_type_forms(self, form_type: str) -> List[CastorForm]:
        """Gets all CastorForms of form_type."""
        forms = self.get_all_forms()
        return [form for form in forms if form.form_type == form_type]

    def get_all_form_type_form_instances(
        self, form_type: str
    ) -> List[CastorFormInstance]:
        """Gets all CastorForms of form_type."""
        instances = self.get_all_form_instances()
        return [
            instance for instance in instances if instance.instance_type == form_type
        ]

    def get_form_instances_by_form(self, form: CastorForm) -> List:
        """Gets all CastorFormInstances that are an instance of the given Form"""
        instances = self.get_all_form_instances()
        return [instance for instance in instances if instance.instance_of == form]

    def get_single_form(self, form_id: str) -> Optional[CastorForm]:
        """Get a single CastorForm based on id."""
        return self.forms_on_id.get(form_id)

    def get_single_form_name(self, form_name: str) -> Optional[CastorForm]:
        """Get a single CastorForm based on id."""
        return self.forms_on_name.get(form_name)

    def add_record(self, record: CastorRecord) -> None:
        """Add a CastorRecord to the study."""
        self.records[record.record_id] = record
        record.study = self

    def get_all_records(self) -> List[CastorRecord]:
        """Get all linked CastorRecords."""
        return list(self.records.values())

    def get_single_record(self, record_id: str) -> Optional[CastorRecord]:
        """Get a single CastorRecord based on id."""
        return self.records.get(record_id)

    def get_all_steps(self) -> List[CastorStep]:
        """Get all linked CastorSteps."""
        steps = list(
            itertools.chain.from_iterable(
                [value.get_all_steps() for key, value in self.forms_on_id.items()]
            )
        )
        return steps

    def get_single_step(self, step_id_or_name: str) -> Optional[CastorStep]:
        """Get a single CastorStep based on id or name."""
        for form in self.get_all_forms():
            # Search for step in each form
            step = form.get_single_step(step_id_or_name)
            # If step found (id and name are both unique)
            if step is not None:
                return step
        # If step not found
        return None

    def get_all_fields(self) -> List[CastorField]:
        """Get all linked CastorFields."""
        fields = list(
            itertools.chain.from_iterable(
                [value.get_all_fields() for key, value in self.forms_on_id.items()]
            )
        )
        return fields

    def get_single_field(self, field_id_or_name: str) -> Optional[CastorField]:
        """Get a single CastorField based on id or name."""
        if field_id_or_name == "":
            # Some Castor studies have fields for which the name can be empty
            # These are nonsensical identifiers, so we can't search on these
            return None
        for form in self.get_all_forms():
            for step in form.get_all_steps():
                # Search for field in each step in each form
                field = step.get_single_field(field_id_or_name)
                # If field found (id and name are both unique)
                if field is not None:
                    return field
        # If field not found
        return None

    def get_all_study_fields(self) -> List[CastorField]:
        """Gets all linked study CastorFields."""
        return self.__get_all_form_type_fields("Study")

    def get_all_survey_fields(self) -> List[CastorField]:
        """Gets all linked survey CastorFields."""
        return self.__get_all_form_type_fields("Survey")

    def get_all_report_fields(self) -> List[CastorField]:
        """Gets all linked report CastorFields."""
        return self.__get_all_form_type_fields("Report")

    def __get_all_form_type_fields(self, form_type: str) -> List[CastorField]:
        """Gets all linked CastorFields belonging to form of form_type."""
        fields = self.get_all_fields()
        return [field for field in fields if field.step.form.form_type == form_type]

    def get_all_form_instances(self) -> List["CastorFormInstance"]:
        """Returns all form instances"""
        form_instances = list(
            itertools.chain.from_iterable(
                [
                    list(value.form_instances_ids.values())
                    for key, value in self.records.items()
                ]
            )
        )
        return form_instances

    def get_single_form_instance_on_id(
        self,
        record_id: str,
        instance_id: str,
    ) -> Optional["CastorFormInstance"]:
        """Returns a single form instance based on id."""
        return self.get_single_record(record_id).get_single_form_instance_on_id(
            instance_id
        )

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the study"""
        data_points = list(
            itertools.chain.from_iterable(
                [value.get_all_data_points() for key, value in self.records.items()]
            )
        )
        return data_points

    def get_single_data_point(
        self, record_id: str, form_instance_id: str, field_id_or_name: str
    ) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id."""
        form_instance = self.get_single_form_instance_on_id(record_id, form_instance_id)
        return form_instance.get_single_data_point(field_id_or_name)

    def instance_of_form(
        self, instance_id: str, instance_type: str
    ) -> Optional[CastorForm]:
        """Returns the form of which the given id is an instance.
        instance_id is id for type: Report, name for type: Survey, or id for type: Study"""
        if instance_type == "Study":
            form = self.get_single_form(instance_id)
        elif instance_type in ("Report", "Survey"):
            form_id = self.form_links[instance_type][instance_id]
            form = self.get_single_form(form_id)
        else:
            raise CastorException(f"{instance_type} is not a form type.")
        return form

    # PRIVATE HELPER FUNCTIONS
    def __link_data(self) -> None:
        """Links the study data"""
        # Get the data from the API
        print("Downloading Study Data.", flush=True, file=sys.stderr)
        data = self.client.export_study_data()

        # Loop over all fields
        for field in tqdm(data, desc="Mapping Data"):
            self.__handle_row(field)

    def __handle_row(self, field):
        """Handles a row from the export data."""
        # Check if the record for the field exists, if not, create it
        record = self.get_single_record(field["Record ID"])
        if record is None:
            record = CastorRecord(record_id=field["Record ID"])
            self.add_record(record)
        if field["Form Type"] == "":
            # If the Form Type is empty, the line indicates a record
            pass
        else:
            # If it is not empty, the line indicates data
            self.__handle_data(field, record)

    def __handle_data(self, field, record):
        """Handles data from a row from the export data"""
        # First check what type of form and check if it exists else create it
        if field["Form Type"] == "Study":
            form_instance = self.__handle_study_form(field, record)
        elif field["Form Type"] == "Report":
            form_instance = self.__handle_report_form(field, record)
        elif field["Form Type"] == "Survey":
            form_instance = self.__handle_survey_form(field, record)
        else:
            raise CastorException(f"Form Type: {field['Form Type']} does not exist.")

        # Check if the field exists, if not, create it
        if field["Field ID"] == "":
            # No field ID means that the row indicates an empty report or survey
            # Empty is a report or survey without any datapoints
            pass
        else:
            self.__handle_data_point(field, form_instance)

    def __handle_data_point(self, field, form_instance):
        """Handles the data point from the export data"""
        # Check if the data point already exists
        # Should not happen, but just in case
        data_point = form_instance.get_single_data_point(field["Field ID"])
        if data_point is None:
            data_point = CastorDataPoint(
                field_id=field["Field ID"],
                raw_value=field["Value"],
                study=self,
                filled_in=field["Date"],
            )
            form_instance.add_data_point(data_point)
        else:
            raise CastorException("Duplicated data point found!")

    def __handle_survey_form(self, field, record):
        form_instance = record.get_single_form_instance_on_id(field["Form Instance ID"])
        if form_instance is None:
            form_instance = CastorSurveyFormInstance(
                instance_id=field["Form Instance ID"],
                name_of_form=field["Form Instance Name"],
                study=self,
            )
            record.add_form_instance(form_instance)
        return form_instance

    def __handle_report_form(self, field, record):
        form_instance = record.get_single_form_instance_on_id(field["Form Instance ID"])
        if form_instance is None:
            form_instance = CastorReportFormInstance(
                instance_id=field["Form Instance ID"],
                name_of_form=field["Form Instance Name"],
                study=self,
            )
            record.add_form_instance(form_instance)
        return form_instance

    def __handle_study_form(self, field, record):
        instance_of_field = self.get_single_field(field["Field ID"])
        instance_of_form = instance_of_field.step.form.form_id
        form_instance_id = instance_of_form
        form_instance = record.get_single_form_instance_on_id(form_instance_id)
        if form_instance is None:
            form_instance = CastorStudyFormInstance(
                instance_id=form_instance_id,
                name_of_form=field["Form Instance Name"],
                study=self,
            )
            record.add_form_instance(form_instance)
        return form_instance

    def __export_study_data(self, archived) -> pd.DataFrame:
        """Returns a dataframe containing all study data."""
        # Get study forms
        forms = self.get_all_form_type_forms("Study")
        df_study = self.__export_data(
            forms,
            [
                "record_id",
                "archived",
                "institute",
                "randomisation_group",
                "randomisation_datetime",
            ],
            "Study",
            archived,
        )
        return df_study

    def __export_survey_data(self, archived) -> Dict[str, pd.DataFrame]:
        """Returns a dict of dataframes containing all survey data."""
        dataframes = {}
        # Get survey forms
        forms = self.get_all_form_type_forms("Survey")
        # For each survey form, create a distinct dataframe
        for form in forms:
            dataframe = self.__export_data(
                [form],
                [
                    "record_id",
                    "institute",
                    "survey_name",
                    "survey_instance_id",
                    "created_on",
                    "sent_on",
                    "progress",
                    "completed_on",
                    "package_id",
                    "package_name",
                    "archived",
                ],
                "Survey",
                archived,
            )
            # Add to return dict
            dataframes[form.form_name] = dataframe
        return dataframes

    def __export_report_data(self, archived):
        """Returns a dict of dataframes containing all report data."""
        dataframes = {}
        # Get survey forms
        forms = self.get_all_form_type_forms("Report")
        # For each survey form, create a distinct dataframe
        for form in forms:
            dataframe = self.__export_data(
                [form],
                [
                    "record_id",
                    "institute",
                    "created_on",
                    "custom_name",
                    "parent",
                    "archived",
                ],
                "Report",
                archived,
            )
            # Add to return dict
            dataframes[form.form_name] = dataframe
        return dataframes

    def __export_data(
        self,
        forms: List["CastorForm"],
        extra_columns: List[str],
        form_type: str,
        archived: bool,
    ) -> pd.DataFrame:
        """Exports given type of data and returns a dataframe."""
        # Get all study fields
        fields = self.__filtered_fields_forms(forms)
        # Get all data points
        if form_type == "Study":
            data = self.__get_all_data_points_study(fields, archived)
        elif form_type == "Survey":
            data = self.__get_all_data_points_survey(forms[0], archived)
        elif form_type == "Report":
            data = self.__get_all_data_points_report(forms[0], archived)
        else:
            raise CastorException(
                f"{form_type} is not a valid type. Use Study/Survey/Report."
            )

        # Order fields
        sorted_fields = sorted(
            fields,
            key=attrgetter("step.form.form_order", "step.step_order", "field_order"),
        )
        # Define columns from study + auxiliary record columns
        column_order = extra_columns + [field.field_name for field in sorted_fields]
        # Convert study data points to data frame
        dataframe = pd.DataFrame.from_records(data, columns=column_order)
        # Split up checkbox and numberdate fields (multiple values in one column)
        dataframe, column_order = self.__split_up_checkbox_data(
            dataframe, fields, column_order
        )
        dataframe, column_order = self.__split_up_numberdate_data(
            dataframe, fields, column_order
        )
        dataframe = self.__format_year(dataframe, fields)
        dataframe = self.__format_categorical_fields(dataframe, fields)
        # Order the dataframe
        dataframe = dataframe[column_order]
        return dataframe

    def __format_categorical_fields(
        self, dataframe: pd.DataFrame, fields: List[CastorField]
    ) -> pd.DataFrame:
        """Sets categorical fields to use categorical dtype."""
        cat_fields = [
            field for field in fields if field.field_type in ["dropdown", "radio"]
        ]
        for field in cat_fields:
            # Get options + missings
            options = self.get_single_optiongroup(field.field_option_group)["options"]
            # Remove duplicates
            option_names = list(
                set(
                    [option["name"] for option in options]
                    + [
                        "measurement failed",
                        "not applicable",
                        "not asked",
                        "asked but unknown",
                        "not done",
                    ]
                )
            )

            # Set columns to categorical
            cat_type = pd.CategoricalDtype(categories=option_names, ordered=False)
            dataframe[field.field_name] = dataframe[field.field_name].astype(cat_type)
        return dataframe

    @staticmethod
    def __format_year(
        dataframe: pd.DataFrame, fields: List[CastorField]
    ) -> pd.DataFrame:
        """Casts year fields to the correct format."""
        # Year fields to Ints
        year_fields = [field for field in fields if field.field_type == "year"]
        for year in year_fields:
            dataframe[year.field_name] = dataframe[year.field_name].astype("Int64")
        return dataframe

    @staticmethod
    def __split_up_numberdate_data(
        dataframe: pd.DataFrame, fields: List[CastorField], column_order: List[str]
    ) -> (pd.DataFrame, List[str]):
        """Splits up the numberdate data in dummies and returns a new dataframe + column order."""
        # Select numberdate fields
        numberdate_fields = [
            field for field in fields if field.field_type == "numberdate"
        ]
        for numberdate in numberdate_fields:
            # Create dummies
            dummies = [
                numberdate.field_name + "_number",
                numberdate.field_name + "_date",
            ]
            # Get an array of the data and double the nans
            temp_list = dataframe[numberdate.field_name].tolist()
            temp_list = [
                [item, item] if not pd.Series(item).any() else item
                for item in temp_list
            ]
            # Add the dummies to the old data frame
            dataframe[dummies] = pd.DataFrame(temp_list, index=dataframe.index)
            # Replace the old column in the order with the new dummy columns
            index = column_order.index(numberdate.field_name)
            column_order.pop(index)
            for dummy in dummies:
                column_order.insert(index, dummy)

        return dataframe, column_order

    def __split_up_checkbox_data(
        self,
        dataframe: pd.DataFrame,
        fields: List[CastorField],
        column_order: List[str],
    ) -> (pd.DataFrame, List[str]):
        """Splits up the checkbox data in dummies and returns a new dataframe + column order."""
        # Select checkbox fields
        checkbox_fields = [field for field in fields if field.field_type == "checkbox"]
        # Create dummies
        dataframe, column_order = self.__create_dummy_columns(
            checkbox_fields, column_order, dataframe
        )
        # Fill in the correct values
        dataframe = self.__update_dummy_values(checkbox_fields, dataframe)
        return dataframe, column_order

    def __update_dummy_values(
        self, checkbox_fields: List, dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """Updates dummy values in a dataframe for checkbox fields."""
        for checkbox in checkbox_fields:
            # Create a dataframe with dummies
            # Cast to string because a completely NaN column throws an error (is float64)
            temp_df = (
                dataframe[checkbox.field_name].astype(str).str.get_dummies(sep="|")
            )

            # Rename the columns
            temp_df.columns = [
                checkbox.field_name + "#" + column for column in temp_df.columns
            ]

            missing_types = {
                checkbox.field_name + "#" + "measurement failed": -95,
                checkbox.field_name + "#" + "not applicable": -96,
                checkbox.field_name + "#" + "not asked": -97,
                checkbox.field_name + "#" + "asked but unknown": -98,
                checkbox.field_name + "#" + "not done": -99,
            }

            # Add the new dummies to the old dataframe, update doesn't add new columns
            dataframe.update(temp_df)

            # Handle user missings and propagate them through all checkbox fields
            options = self.get_single_optiongroup(checkbox.field_option_group)[
                "options"
            ]
            option_names = [option["name"] for option in options]

            # Create new columns for these dummies
            new_column_names = [
                checkbox.field_name + "#" + option_name for option_name in option_names
            ]

            # Set all dummy columns to missing if one of the missings is True
            for missing_type, value in missing_types.items():
                try:
                    dataframe.loc[temp_df[missing_type] == 1, new_column_names] = value
                except KeyError:
                    pass

            # Set columns to categorical
            cat_type = pd.CategoricalDtype(
                categories=[0, 1, -95, -96, -97, -98, -99], ordered=False
            )
            for column in new_column_names:
                dataframe[column] = dataframe[column].astype(cat_type)

        return dataframe

    def __create_dummy_columns(
        self, checkbox_fields: List, column_order: List, dataframe: pd.DataFrame
    ) -> (pd.DataFrame, List):
        """Creates dummy columns in the dataframe for all checkbox fields"""
        # Get all possible dummies
        for checkbox in checkbox_fields:
            options = self.get_single_optiongroup(checkbox.field_option_group)[
                "options"
            ]
            option_names = [option["name"] for option in options]

            # Create new columns for these dummies
            new_column_names = [
                checkbox.field_name + "#" + option_name for option_name in option_names
            ]
            dataframe = dataframe.reindex(
                columns=dataframe.columns.tolist() + new_column_names, fill_value=0
            )

            # Replace the old column in the order with the new dummy columns
            index = column_order.index(checkbox.field_name)
            column_order.pop(index)
            for dummy in new_column_names:
                column_order.insert(index, dummy)

        return dataframe, column_order

    @staticmethod
    def __filtered_fields_forms(forms: List[CastorForm]) -> List["CastorField"]:
        """Returns all informational fields belonging to certain form types."""
        # Get the form fields
        fields = list(
            itertools.chain.from_iterable([form.get_all_fields() for form in forms])
        )
        # Filter out remark fields
        filtered_fields = [
            field
            for field in fields
            if field.field_type
            not in (
                "remark",
                "repeated_measures",
                "add_report_button",
                "summary",
                "image",
            )
        ]
        return filtered_fields

    def __get_all_data_points_study(self, fields: List, archived: bool) -> List[dict]:
        """Returns a list of dicts of all study data points."""
        # Get all records
        records = self.get_all_records()
        data = []

        for record in records:
            # Test whether data points should be extracted
            if archived or not record.archived:
                data_points = record.get_all_data_points()
                filtered_data_points = [
                    data_point
                    for data_point in data_points
                    if data_point.instance_of in fields
                ]
                record_data = {
                    data_point.instance_of.field_name: data_point.value
                    for data_point in filtered_data_points
                }
                record_data["record_id"] = record.record_id
                record_data["institute"] = record.institute
                record_data["randomisation_group"] = record.randomisation_group
                record_data["randomisation_datetime"] = record.randomisation_datetime
                record_data["archived"] = record.archived
                data.append(record_data)

        return data

    def __get_all_data_points_survey(
        self, form: "CastorForm", archived: bool
    ) -> List[dict]:
        """Returns a list of dicts of all survey data points."""
        data = []
        form_instances = self.get_form_instances_by_form(form)
        for instance in form_instances:
            # Test whether data points should be extracted
            if archived or not (instance.record.archived or instance.archived):
                # Get all data points and select only relevant ones
                data_points = instance.get_all_data_points()
                # Report data
                record_form_data = {
                    data_point.instance_of.field_name: data_point.value
                    for data_point in data_points
                }
                # Auxiliary data
                record_form_data["record_id"] = instance.record.record_id
                record_form_data["institute"] = instance.record.institute
                record_form_data["survey_name"] = instance.name_of_form
                record_form_data["survey_instance_id"] = instance.instance_id
                record_form_data["created_on"] = instance.created_on
                record_form_data["sent_on"] = instance.sent_on
                record_form_data["progress"] = instance.progress
                record_form_data["completed_on"] = instance.completed_on
                record_form_data["package_id"] = instance.survey_package_id
                record_form_data["package_name"] = instance.survey_package_name
                record_form_data["archived"] = instance.archived

                # Add to data
                data.append(record_form_data)

        return data

    def __get_all_data_points_report(
        self, form: "CastorForm", archived: bool
    ) -> List[dict]:
        """Returns a list of dicts of all report data points."""
        data = []
        form_instances = self.get_form_instances_by_form(form)
        for instance in form_instances:
            # Test whether data points should be extracted
            if archived or not (instance.record.archived or instance.archived):
                # Get all data points and select only relevant ones
                data_points = instance.get_all_data_points()
                # Report data
                record_form_data = {
                    data_point.instance_of.field_name: data_point.value
                    for data_point in data_points
                }
                # Auxiliary data
                record_form_data["record_id"] = instance.record.record_id
                record_form_data["institute"] = instance.record.institute
                record_form_data["created_on"] = instance.created_on
                record_form_data["custom_name"] = instance.name_of_form
                record_form_data["parent"] = instance.parent
                record_form_data["archived"] = instance.archived

                # Add to data
                data.append(record_form_data)

        return data

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorStudy):
            return NotImplemented
        return self.study_id == other.study_id

    def __repr__(self) -> str:
        return self.study_id
