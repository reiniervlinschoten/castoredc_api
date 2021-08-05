import itertools
import pathlib
import re

import numpy as np
import pandas as pd

from datetime import datetime
from operator import attrgetter
from typing import List, Optional, Any, Union, Dict
from pandas import CategoricalDtype
from tqdm import tqdm

from castoredc_api_client import CastorException
from castoredc_api_client.castoredc_api_client import CastorClient
from castoredc_api_study.castor_objects.castor_data_point import CastorDataPoint
from castoredc_api_study.castor_objects.castor_field import CastorField
from castoredc_api_study.castor_objects.castor_form_instance import CastorFormInstance
from castoredc_api_study.castor_objects.castor_record import CastorRecord
from castoredc_api_study.castor_objects.castor_step import CastorStep
from castoredc_api_study.castor_objects.castor_form import CastorForm


class CastorStudy:
    """Object representing a study in Castor. Functions as the head of a tree for all interrelations.
    Needs an authenticated api_client that is linked to the same study_id to call data."""

    def __init__(
        self, client_id: str, client_secret: str, study_id: str, url: str, test=False
    ) -> None:
        """Create a CastorStudy object."""
        self.study_id = study_id
        # Create the client to interact with the study
        if test is False:
            self.client = CastorClient(client_id, client_secret, url)
            self.client.link_study(study_id)

        # List of all forms in the study - structure
        self.forms = []
        # List of all records in the study - data
        self.records = []

        # Dictionary of dicts to store the relationship between a form ID and a list of form instances
        self.form_links = {}
        # List of dictionaries of optiongroups
        self.optiongroups = []

        # Container variables to save time querying the database
        self.__all_report_instances = []

    # STRUCTURE MAPPING
    def map_structure(self) -> None:
        """Returns a CastorStudy object with the corresponding variable tree depicting interrelations"""
        # Reset structure & data
        self.forms = []
        self.records = []
        self.form_links = {}

        # Get the structure from the API
        print("Downloading study structure.")
        data = self.client.export_study_structure()

        # Loop over all fields
        for field in tqdm(data, desc="Mapping Fields"):
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

            # Check if the field exists, if not, create it
            # This should not be possible as there are no doubles, but checking just in case
            new_field = step.get_single_field(field["Field ID"])
            if new_field is None:
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

        self.__map_field_dependencies()

    # DATA MAPPING
    def map_data(self) -> None:
        """Imports the data from the CastorClient database, maps the interrelations and links it to the study."""
        self.map_structure()
        self.update_links()
        self.__link_data()
        self.__interpret_values()
        self.__load_record_information()
        self.__load_survey_information()
        self.__load_report_information()

    def update_links(self) -> None:
        """Creates the links between form and form instances."""
        # Reset form links
        self.form_links = {}

        form_links = {"Survey": {}, "Report": {}}

        # Get all survey forms that need to be linked
        survey_forms = self.get_all_survey_forms()
        for form in survey_forms:
            form_links["Survey"][form.form_id] = []

        # Get the name of the survey forms, as the export data can only be linked on name, not on id
        print("Downloading survey instances.")
        surveys = self.client.all_surveys()
        # Link form id to form name
        for survey in tqdm(surveys, desc="Mapping Survey Instances"):
            form_links["Survey"][survey["id"]].append(survey["name"])

        # Get all report forms that need to be linked
        report_forms = self.get_all_report_forms()
        for form in report_forms:
            form_links["Report"][form.form_id] = []

        # Get all report instances that need to be linked
        print("Downloading report instances.")

        # Save this data from the database to save time later
        report_instances = self.client.all_report_instances(archived=0)
        archived_report_instances = self.client.all_report_instances(archived=1)
        self.__all_report_instances = report_instances + archived_report_instances

        # Link instance to form on id
        for instance in tqdm(
            self.__all_report_instances, desc="Mapping Report Instances"
        ):
            form_links["Report"][instance["_embedded"]["report"]["id"]].append(
                instance["id"]
            )

        self.form_links = form_links

    # OPTIONGROUPS
    def load_optiongroups(self) -> None:
        """Loads all optiongroups through the client"""
        # Get the optiongroups
        print("Downloading optiongroups.")
        self.optiongroups = self.client.all_field_optiongroups()

    # AUXILIARY DATA
    def __load_record_information(self) -> None:
        """Adds auxiliary data to records."""
        print("Downloading record information.")
        record_data = self.client.all_records()
        for record in tqdm(self.records, desc="Augmenting Record Data"):
            record_api = next(
                (
                    _record
                    for _record in record_data
                    if _record["id"] == record.record_id
                ),
                None,
            )
            record.institute = record_api["_embedded"]["institute"]["name"]
            record.randomisation_group = record_api["randomization_group_name"]
            record.randomisation_datetime = self.__get_date_or_none(
                record_api["randomized_on"]
            )

    def __load_survey_information(self) -> None:
        """Adds auxiliary data to survey forms."""
        print("Downloading survey information.")
        survey_package_data = (
            self.client.all_survey_package_instances()
        )  # TODO: this call takes ~30s, optimise?
        survey_form_instances = [
            instance
            for instance in self.get_all_form_instances()
            if instance.instance_of.form_type == "Survey"
        ]
        for form_instance in tqdm(survey_form_instances, desc="Augmenting Survey Data"):
            # TODO: ugly, refactor
            # Now finds survey_instance_id somewhere far embedded in the data returned by the survey package instances
            # and returns the overlying survey package instance
            parent_package = next(
                (
                    package
                    for package in survey_package_data
                    if form_instance.instance_id
                    in [
                        survey["id"]
                        for survey in package["_embedded"]["survey_instances"]
                    ]
                ),
                None,
            )
            form_instance.created_on = datetime.strptime(
                parent_package["created_on"]["date"], "%Y-%m-%d %H:%M:%S.%f"
            )
            form_instance.sent_on = self.__get_date_or_none(parent_package["sent_on"])
            form_instance.progress = next(
                (
                    survey
                    for survey in parent_package["_embedded"]["survey_instances"]
                    if survey["id"] == form_instance.instance_id
                ),
                None,
            )["progress"]
            form_instance.completed_on = self.__get_date_or_none(
                parent_package["finished_on"]
            )
            form_instance.archived = parent_package["archived"]
            # TODO: decide if we want this in output, Castor doesn't
            # form_instance.survey_package_id = parent_package["id"]

    def __load_report_information(self) -> None:
        """Adds auxiliary data to report forms."""
        report_instances = [
            instance
            for instance in self.get_all_form_instances()
            if instance.instance_of in self.get_all_report_forms()
        ]
        for form_instance in tqdm(report_instances, "Augmenting Report Data"):
            report_information = next(
                (
                    instance
                    for instance in self.__all_report_instances
                    if form_instance.instance_id == instance["id"]
                ),
                None,
            )
            form_instance.created_on = datetime.strptime(
                report_information["created_on"], "%Y-%m-%d %H:%M:%S"
            )
            form_instance.parent = (
                "No parent"
                if report_information["parent_id"] == ""
                else self.get_single_form(report_information["parent_id"]).form_name
            )
            form_instance.archived = report_information["archived"]

    @staticmethod
    def __get_date_or_none(dictionary: Optional[dict]) -> Optional[datetime]:
        """Returns the date or None when no date found."""
        date = (
            None
            if dictionary is None
            else datetime.strptime(dictionary["date"], "%Y-%m-%d %H:%M:%S.%f")
        )
        return date

    # FIELD DEPENDENCIES
    def __map_field_dependencies(self) -> None:
        """Retrieves all field_dependencies and links them to the right field."""
        print("Downloading field dependencies.")
        dependencies = self.client.all_field_dependencies()
        # Format to dict of {child_id: {"parent_field": parent_field, "parent_value": value}
        dependencies = {
            dep["child_id"]: {
                "parent_field": self.get_single_field(dep["parent_id"]),
                "parent_value": dep["value"],
            }
            for dep in dependencies
        }
        for child_id in tqdm(dependencies, desc="Mapping Dependencies"):
            self.get_single_field(child_id).field_dependency = dependencies[child_id]

    # DATA INTERPRETATION
    def __interpret_values(self) -> None:
        """Interprets all datapoints in the study in preparation of data export."""
        self.load_optiongroups()
        for field in tqdm(self.get_all_data_points(), desc="Interpreting Values"):
            field.interpret()

    # DATA ANALYSIS
    def export_to_dataframe(self) -> dict:
        """Exports all data from a study into a dict of dataframes for statistical analysis."""
        self.map_data()
        dataframes = {
            "Study": self.__export_study_data(),
            "Surveys": self.__export_survey_data(),
            "Reports": self.__export_report_data(),
        }
        return dataframes

    def export_to_csv(self) -> str:
        """Exports all data to csv files, returns string of time ran for testing purposes and file finding."""
        now = f"{datetime.now().strftime('%Y%m%d %H%M%S')}"
        date_format = "%d-%m-%Y %H:%M:%S"
        dataframes = self.export_to_dataframe()
        pathlib.Path(pathlib.Path.cwd(), "output").mkdir(parents=True, exist_ok=True)
        dataframes["Study"].to_csv(
            path_or_buf=pathlib.Path(
                pathlib.Path.cwd(), "output", f"{now} {self.study_id} Study.csv"
            ),
            sep=";",
            index=False,
            date_format=date_format,
        )
        for dataframe in dataframes["Surveys"]:
            filename = re.sub("[^\w\-_\. ]", "_", dataframe)
            dataframes["Surveys"][dataframe].to_csv(
                path_or_buf=pathlib.Path(
                    pathlib.Path.cwd(),
                    "output",
                    f"{now} {self.study_id} {filename}.csv",
                ),
                sep=";",
                index=False,
                date_format=date_format,
            )

        for dataframe in dataframes["Reports"]:
            filename = re.sub("[^\w\-_\. ]", "_", dataframe)
            dataframes["Reports"][dataframe].to_csv(
                path_or_buf=pathlib.Path(
                    pathlib.Path.cwd(),
                    "output",
                    f"{now} {self.study_id} {filename}.csv",
                ),
                sep=";",
                index=False,
                date_format=date_format,
            )
        return now

    def export_to_feather(self) -> dict:
        """Exports all data to feather files, returns dict of file locations for export into R."""
        dataframes = self.export_to_dataframe()
        pathlib.Path(pathlib.Path.cwd(), "output").mkdir(parents=True, exist_ok=True)
        dataframes["Study"].reset_index().to_feather(
            pathlib.Path(pathlib.Path.cwd(), "output", "Study.feather"),
            compression="uncompressed",
        )
        dataframes["Study"] = str(
            pathlib.Path(pathlib.Path.cwd(), "output", "Study.feather")
        )

        for report in dataframes["Reports"]:
            dataframes["Reports"][report].reset_index().to_feather(
                pathlib.Path(pathlib.Path.cwd(), "output", f"{report}.feather"),
                compression="uncompressed",
            )
            dataframes["Reports"][report] = str(
                pathlib.Path(pathlib.Path.cwd(), "output", f"{report}.feather")
            )

        for survey in dataframes["Surveys"]:
            dataframes["Surveys"][survey].reset_index().to_feather(
                pathlib.Path(pathlib.Path.cwd(), "output", f"{survey}.feather"),
                compression="uncompressed",
            )
            dataframes["Surveys"][survey] = str(
                pathlib.Path(pathlib.Path.cwd(), "output", f"{survey}.feather")
            )

        return dataframes

    # HELPERS
    def get_single_optiongroup(self, optiongroup_id: str) -> Optional[Dict]:
        """Get a single optiongroup based on id."""
        return next(
            (group for group in self.optiongroups if group["id"] == optiongroup_id),
            None,
        )

    def add_form(self, form: CastorForm) -> None:
        """Add a CastorForm to the study."""
        self.forms.append(form)
        form.study = self

    def get_all_forms(self) -> List[CastorForm]:
        """Get all linked CastorForms."""
        return self.forms

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

    def get_form_instances_by_form(self, form: CastorForm) -> List[CastorFormInstance]:
        """Gets all CastorFormInstances that are an instance of the given Form"""
        instances = self.get_all_form_instances()
        return [instance for instance in instances if instance.instance_of == form]

    def get_single_form(self, form_id_or_name: str) -> Optional[CastorForm]:
        """Get a single CastorForm based on id or name."""
        return next(
            (
                form
                for form in self.forms
                if (
                    form.form_id == form_id_or_name or form.form_name == form_id_or_name
                )
            ),
            None,
        )

    def add_record(self, record: CastorRecord) -> None:
        """Add a CastorRecord to the study."""
        self.records.append(record)
        record.study = self

    def get_all_records(self) -> List[CastorRecord]:
        """Get all linked CastorRecords."""
        return self.records

    def get_single_record(self, record_id: str) -> Optional[CastorRecord]:
        """Get a single CastorRecord based on id."""
        return next(
            (record for record in self.records if record.record_id == record_id), None
        )

    def get_all_steps(self) -> List[CastorStep]:
        """Get all linked CastorSteps."""
        steps = list(
            itertools.chain.from_iterable([_form.steps for _form in self.forms])
        )
        return steps

    def get_single_step(self, step_id_or_name: str) -> Optional[CastorStep]:
        """Get a single CastorStep based on id or name."""
        steps = self.get_all_steps()
        return next(
            (
                step
                for step in steps
                if (
                    step.step_id == step_id_or_name or step.step_name == step_id_or_name
                )
            ),
            None,
        )

    def get_all_fields(self) -> List[CastorField]:
        """Get all linked CastorFields."""
        fields = list(
            itertools.chain.from_iterable(
                [form.get_all_fields() for form in self.forms]
            )
        )
        return fields

    def get_single_field(self, field_id_or_name: str) -> Optional[CastorField]:
        """Get a single CastorField based on id."""
        fields = self.get_all_fields()
        return next(
            (
                field
                for field in fields
                if (
                    field.field_id == field_id_or_name
                    or field.field_name == field_id_or_name
                )
            ),
            None,
        )

    def get_all_study_fields(self) -> List[CastorField]:
        """Gets all linked study CastorFields."""
        return self.get_all_form_type_fields("Study")

    def get_all_survey_fields(self) -> List[CastorField]:
        """Gets all linked survey CastorFields."""
        return self.get_all_form_type_fields("Survey")

    def get_all_report_fields(self) -> List[CastorField]:
        """Gets all linked report CastorFields."""
        return self.get_all_form_type_fields("Report")

    def get_all_form_type_fields(self, form_type: str) -> List[CastorField]:
        """Gets all linked CastorFields belonging to form of form_type."""
        fields = self.get_all_fields()
        return [field for field in fields if field.step.form.form_type == form_type]

    def get_all_form_instances(self) -> List["CastorFormInstance"]:
        """Returns all form instances"""
        form_instances = list(
            itertools.chain.from_iterable(
                [_record.form_instances for _record in self.records]
            )
        )
        return form_instances

    def get_single_form_instance(
        self, record_id: str, instance_id: str,
    ) -> Optional["CastorFormInstance"]:
        """Returns a single form instance based on id."""
        record = self.get_single_record(record_id)
        all_form_instances = record.get_all_form_instances()
        return next(
            (
                instance
                for instance in all_form_instances
                if instance.instance_id == instance_id
            ),
            None,
        )

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the study"""
        data_points = list(
            itertools.chain.from_iterable(
                [_record.get_all_data_points() for _record in self.records]
            )
        )
        return data_points

    def get_single_data_point(
        self, record_id: str, form_instance_id: str, field_id_or_name: str
    ) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id."""
        form_instance = self.get_single_form_instance(record_id, form_instance_id)
        return form_instance.get_single_data_point(field_id_or_name)

    def instance_of_form(
        self, instance_id: str, instance_type: str
    ) -> Optional[CastorForm]:
        """Returns the form of which the given id is an instance.
        instance_id is id for type: Report, name for type: Survey, or id for type: Study"""
        if instance_type == "Study":
            return self.get_single_form(instance_id)
        elif instance_type == "Report" or instance_type == "Survey":
            options = self.form_links[instance_type]
            form_id = next(
                (form_id for form_id in options if instance_id in options[form_id]),
                None,
            )
            return self.get_single_form(form_id)
        else:
            raise CastorException("{} is not a form type.".format(instance_type))

    # PRIVATE HELPER FUNCTIONS
    def __link_data(self) -> None:
        """Links the study data"""
        # Get the data from the API
        print("Downloading study data.")
        data = self.client.export_study_data()

        # Loop over all fields
        for field in tqdm(data, desc="Mapping Data"):
            # Check if the record for the field exists, if not, create it
            record = self.get_single_record(field["Record ID"])
            if record is None:
                record = CastorRecord(record_id=field["Record ID"])
                self.add_record(record)

            # Check if it a data line or a record line
            if field["Form Type"] == "":
                pass
            else:
                if field["Form Type"] == "Study":
                    instance_of_field = self.get_single_field(field["Field ID"])
                    instance_of_form = instance_of_field.step.form.form_id
                    form_instance_id = instance_of_form
                    form_instance = record.get_single_form_instance(form_instance_id)
                    if form_instance is None:
                        form_instance = CastorFormInstance(
                            instance_id=form_instance_id,
                            instance_type=field["Form Type"],
                            name_of_form=field["Form Instance Name"],
                            study=self,
                        )
                        record.add_form_instance(form_instance)

                else:
                    form_instance = record.get_single_form_instance(
                        field["Form Instance ID"]
                    )
                    if form_instance is None:
                        form_instance = CastorFormInstance(
                            instance_id=field["Form Instance ID"],
                            instance_type=field["Form Type"],
                            name_of_form=field["Form Instance Name"],
                            study=self,
                        )
                        record.add_form_instance(form_instance)

                # Check if the field exists, if not, create it
                # This should not be possible as there are no doubles, but checking just in case
                data_point = form_instance.get_single_data_point(field["Field ID"])
                if data_point is None:
                    data_point = CastorDataPoint(
                        field_id=field["Field ID"],
                        raw_value=field["Value"],
                        study=self,
                        filled_in=field["Date"],
                    )
                    form_instance.add_data_point(data_point)

    def __export_study_data(self) -> pd.DataFrame:
        """Returns a dataframe containing all study data."""
        # Get study forms
        forms = self.get_all_form_type_forms("Study")
        df_study = self.__export_data(
            forms,
            ["record_id", "institute", "randomisation_group", "randomisation_datetime"],
            "Study",
        )
        return df_study

    def __export_survey_data(self) -> Dict[str, pd.DataFrame]:
        """Returns a dict of dataframes containing all survey data."""
        dataframes = {}
        # Get survey forms
        forms = self.get_all_form_type_forms("Survey")
        # For each survey form, create a distinct dataframe
        for form in forms:
            df = self.__export_data(
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
                    "archived",
                ],
                "Survey",
            )
            # Add to return dict
            dataframes[form.form_name] = df
        return dataframes

    def __export_report_data(self):
        """Returns a dict of dataframes containing all report data."""
        dataframes = {}
        # Get survey forms
        forms = self.get_all_form_type_forms("Report")
        # For each survey form, create a distinct dataframe
        for form in forms:
            df = self.__export_data(
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
            )
            # Add to return dict
            dataframes[form.form_name] = df
        return dataframes

    def __export_data(
        self, forms: List["CastorForm"], extra_columns: List[str], form_type: str
    ) -> pd.DataFrame:
        """Exports given type of data and returns a dataframe."""
        # Get all study fields
        fields = self.__filtered_fields_forms(forms)
        # Get all data points
        if form_type == "Study":
            data = self.__get_all_data_points_study(fields)
        elif form_type == "Survey":
            data = self.__get_all_data_points_survey(fields)
        elif form_type == "Report":
            data = self.__get_all_data_points_report(fields)
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
        df = pd.DataFrame.from_records(data, columns=column_order)
        # Split up checkbox and numberdate fields (multiple values in one column)
        df, column_order = self.__split_up_checkbox_data(df, fields, column_order)
        df, column_order = self.__split_up_numberdate_data(df, fields, column_order)
        df = self.__format_year_and_date(df, fields)
        df = self.__format_categorical_fields(df, fields)
        # Order the dataframe
        df = df[column_order]
        return df

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
            option_names = [option["name"] for option in options] + [
                "measurement failed",
                "not applicable",
                "not asked",
                "asked but unknown",
                "not done",
            ]

            # Set columns to categorical
            cat_type = CategoricalDtype(categories=option_names, ordered=False)
            dataframe[field.field_name] = dataframe[field.field_name].astype(cat_type)
        return dataframe

    def __format_year_and_date(
        self, dataframe: pd.DataFrame, fields: List[CastorField]
    ) -> pd.DataFrame:
        """Casts year fields to the correct format."""
        # Year fields to Ints
        year_fields = [field for field in fields if field.field_type == "year"]
        for year in year_fields:
            dataframe[year.field_name] = dataframe[year.field_name].astype("Int64")

        # # Date fields to string
        # date_fields = [field for field in fields if field.field_type == "date"]
        # for date in date_fields:
        #     # Work-around, as Pandas can't handle large dates.
        #     dataframe[date.field_name] = dataframe[date.field_name].astype(str).apply(self.__convert_dates)

        return dataframe

    @staticmethod
    def __convert_dates(date: str) -> str:
        """Converts dates in Castor notation (yyyy-mm-dd hh:mm:ss) to dd-mm-yyy."""
        if pd.isnull(date) or date in ["NaT", "NaN", "nan"]:
            return np.nan
        else:
            return pd.Period(
                year=int(date[:4]), month=int(date[5:7]), day=int(date[8:10]), freq="D"
            ).strftime("%d-%m-%Y")

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
            for missing_type in missing_types:
                try:
                    dataframe.loc[
                        temp_df[missing_type] == 1, new_column_names
                    ] = missing_types[missing_type]
                except KeyError:
                    pass

            # Set columns to categorical
            cat_type = CategoricalDtype(
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
        """Returns all fields belonging to certain form types and filters out non informational fields fields."""
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

    def __get_all_data_points_study(self, fields: List) -> List[dict]:
        """Loop over all records and returns a list of dicts of all data points corresponding to fields."""
        # Get all records
        records = self.get_all_records()
        data = []

        for record in records:
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
            data.append(record_data)

        return data

    def __get_all_data_points_survey(self, fields: List) -> List[dict]:
        """Loop over all records and returns a list of dicts of all data points corresponding to fields."""
        # Get all records
        records = self.get_all_records()
        data = []
        # TODO: Add empty surveys, these are not found because they have no datapoints.

        for record in records:
            # Get all data points and select only relevant ones
            data_points = record.get_all_data_points()
            filtered_data_points = [
                data_point
                for data_point in data_points
                if data_point.instance_of in fields
            ]
            # Sort data points by form_instance and then group by form instance
            sorted_data_points = sorted(
                filtered_data_points, key=attrgetter("form_instance.instance_id")
            )
            for form_instance, data_points in itertools.groupby(
                sorted_data_points, lambda data_point: data_point.form_instance
            ):
                # Survey data
                record_form_data = {
                    data_point.instance_of.field_name: data_point.value
                    for data_point in data_points
                }
                # Auxiliary data
                record_form_data["record_id"] = record.record_id
                record_form_data["institute"] = record.institute
                record_form_data["survey_name"] = form_instance.name_of_form
                record_form_data["survey_instance_id"] = form_instance.instance_id
                record_form_data["created_on"] = form_instance.created_on
                record_form_data["sent_on"] = form_instance.sent_on
                record_form_data["progress"] = form_instance.progress
                record_form_data["completed_on"] = form_instance.completed_on
                record_form_data["package_id"] = form_instance.survey_package_id
                record_form_data["archived"] = form_instance.archived
                # Add to data
                data.append(record_form_data)

        return data

    def __get_all_data_points_report(self, fields: List) -> List[dict]:
        """Loop over all records and returns a list of dicts of all data points corresponding to fields."""
        # Get all records
        records = self.get_all_records()
        data = []
        # TODO: Add empty reports, these are not found because they have no datapoints.

        for record in records:
            # Get all data points and select only relevant ones
            data_points = record.get_all_data_points()
            filtered_data_points = [
                data_point
                for data_point in data_points
                if data_point.instance_of in fields
            ]
            # Sort data points by form_instance and then group by form instance
            sorted_data_points = sorted(
                filtered_data_points, key=attrgetter("form_instance.instance_id")
            )
            for form_instance, data_points in itertools.groupby(
                sorted_data_points, lambda data_point: data_point.form_instance
            ):
                # Report data
                record_form_data = {
                    data_point.instance_of.field_name: data_point.value
                    for data_point in data_points
                }
                # Auxiliary data
                record_form_data["record_id"] = record.record_id
                record_form_data["institute"] = record.institute
                record_form_data["created_on"] = form_instance.created_on
                record_form_data["custom_name"] = form_instance.name_of_form
                record_form_data["parent"] = form_instance.parent
                record_form_data["archived"] = form_instance.archived

                # Add to data
                data.append(record_form_data)

        return data

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorStudy):
            return NotImplemented
        else:
            return self.study_id == other.study_id

    def __repr__(self) -> str:
        return self.study_id
