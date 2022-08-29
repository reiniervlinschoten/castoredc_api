"""Module for interacting with the Castor EDC API."""

import asyncio
import csv
import json
import sys
from datetime import datetime
from itertools import chain
from typing import List, Optional, Union

import httpx
from httpx import HTTPStatusError
from tqdm import tqdm

if sys.version_info >= (3, 8):
    from importlib import metadata as pkg_metadata
else:
    import importlib_metadata as pkg_metadata


class CastorException(Exception):
    """Exception class for interacting with Castor database"""


class CastorClient:
    """Object to connect and interact with Castor EDC API"""

    # pylint: disable=too-many-arguments
    # Necessary number of arguments to interact with API
    # pylint: disable=too-many-public-methods
    # Necessary number of public methods to interact with API

    # INITIALIZATION
    # Limits for server load
    max_connections = 15
    timeout = httpx.Timeout(10.0, read=60)
    limits = httpx.Limits(max_connections=max_connections)

    def __init__(self, client_id, client_secret, url):
        """Create a CastorClient to communicate with a Castor database.
        Links the CastorClient to an account with client_id and client_secret.
        URL determines which server is connected to."""
        # Instantiate URLs
        self.base_url = f"https://{url}/api"
        self.auth_url = f"https://{url}/oauth/token"

        try:
            self.package_version = pkg_metadata.version("castoredc_api")
        except pkg_metadata.PackageNotFoundError:
            self.package_version = "dev"

        # Instantiate client
        self.client = httpx.Client(
            headers={
                "accept": "*/*",  # "application/hal+json; text/csv",
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": f"python-castoredc_api/{self.package_version}",
            },
            limits=self.limits,
            timeout=self.timeout,
        )

        # Grab authentication token for given client
        token = self.request_auth_token(client_id, client_secret)
        self.client.headers["authorization"] = "Bearer " + token

        # Instantiate global study variables
        self.study_url = None

    def link_study(self, study_id):
        """Link a study based on the study_id."""
        self.study_url = self.base_url + "/study/" + study_id

    # API ENDPOINTS
    # AUDIT TRAIL
    def audit_trail(
        self,
        date_from: Union[str, datetime],
        date_to: Union[str, datetime],
        user_id: Optional[str] = None,
        event_types: Optional[List] = None,
    ):
        """Returns a dict of the audit trail.
        date_from and date_to need to be a datetime object or strings formatted as yyyy-mm-dd."""
        url = self.study_url + "/audit-trail"
        # Format and validate dates
        if isinstance(date_from, str):
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
        if isinstance(date_to, str):
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        params = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
        }
        if user_id:
            params["user_id"] = user_id
        if event_types:
            params["event_types"] = ",".join(event_types)
        return self.sync_get(url, params)["items"]

    # COUNTRY
    def all_countries(self):
        """Returns a list of dicts of all available countries."""
        endpoint = "/country"
        raw_data = self.retrieve_general_data(endpoint=endpoint)
        return raw_data["results"]

    def single_country(self, country_id):
        """Returns a dict with the given country based on country_id."""
        endpoint = f"/country/{country_id}"
        return self.retrieve_general_data(endpoint=endpoint)

    # DATA-POINT-COLLECTION GET (STUDY)
    def all_study_data_points(self):
        """Returns a list of dicts of all filled in study data."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/data-point-collection/study", data_name="items"
        )

    def all_report_data_points(self):
        """Returns a list of dicts all filled in report data."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/data-point-collection/report-instance", data_name="items"
        )

    def all_survey_data_points(self):
        """Returns a list of dicts all filled in survey data."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/data-point-collection/survey-instance", data_name="items"
        )

    # DATA-POINT-COLLECTION GET (INSTANCE)
    def single_report_instance_data_points(self, report_id):
        """Returns a list of the data for given report_id."""
        url = f"/data-point-collection/report-instance/{report_id}"
        return self.retrieve_data_points(url)

    def single_survey_instance_data_points(self, survey_instance_id):
        """Returns a list of data from a single survey instance id."""
        url = f"/data-point-collection/survey-instance/{survey_instance_id}"
        return self.retrieve_data_points(url)

    def single_survey_package_instance_data_points(self, survey_package_instance_id):
        """Returns a list of data from a single survey package instance.
        Returns None if package not found."""
        url = f"/data-point-collection/survey-package-instance/{survey_package_instance_id}"
        return self.retrieve_data_points(url)

    # DATA-POINT-COLLECTION GET (RECORD)
    def all_study_data_points_record(self, record_id):
        """Returns a list of all study data collected for given record.
        Returns None if record not found."""
        url = f"/record/{record_id}/data-point-collection/study"
        return self.retrieve_data_points(url)

    def all_report_data_points_record(self, record_id):
        """Returns a list of all report data collected for given record.
        Returns None if record not found."""
        url = f"/record/{record_id}/data-point-collection/report-instance"
        return self.retrieve_data_points(url)

    def single_report_data_points_record(self, record_id, report_id):
        """Returns a list of the data for given report_id for given.
        Returns None if record or report not found."""
        url = f"/record/{record_id}/data-point-collection/report-instance/{report_id}"
        return self.retrieve_data_points(url)

    def all_survey_data_points_record(self, record_id):
        """Returns a list of all survey data collected for given record.
        Returns None if record not found."""
        url = f"/record/{record_id}/data-point-collection/survey-instance"
        return self.retrieve_data_points(url)

    def single_survey_data_points_record(self, record_id, survey_instance_id):
        """Returns a list of data from a single survey instance
        collected for given record record_id. Returns None if record not found."""
        url = f"/record/{record_id}/data-point-collection/survey-instance/{survey_instance_id}"
        return self.retrieve_data_points(url)

    def single_survey_package_data_points_record(
        self, record_id, survey_package_instance_id
    ):
        """Returns a list of data from a single survey package instance
        collected for given record record_id. Returns None if record not found"""
        url = (
            f"/record/{record_id}/data-point-collection/"
            f"survey-package-instance/{survey_package_instance_id}"
        )
        return self.retrieve_data_points(url)

    # DATA-POINT-COLLECTION POST (RECORD)
    def update_study_data_record(self, record_id, common, body):
        """Creates/updates a collection of field values.
        Returns None if record not found.
        Post Data Models:
        Common: {
            "change_reason": "string",
            "confirmed_changes": boolean
                }
        Body: [{
            "field_id": "string",
            "field_value": "string",
            "change_reason": "string",
            "confirmed_changes": boolean
                }]
        """
        url = self.study_url + f"/record/{record_id}/data-point-collection/study"
        post_data = {"common": common, "data": body}
        return self.sync_post(url, post_data)

    def update_report_data_record(self, record_id, report_id, common, body):
        """Creates/updates a report instance.
        Returns None if record not found.
        Post Data Models:
        Common: {
            "change_reason": "string",
            "confirmed_changes": boolean
                }
        Body: [{
            "field_id": "string",
            "instance_id": "string",
            "field_value": "string",
            "change_reason": "string",
            "confirmed_changes": boolean
                }]
        """
        url = (
            self.study_url
            + f"/record/{record_id}/data-point-collection/report-instance/{report_id}"
        )
        post_data = {"common": common, "data": body}
        return self.sync_post(url, post_data)

    def update_survey_instance_data_record(
        self, record_id, survey_instance_id, body, change_reason
    ):
        """Creates/updates a survey instance.
        Returns None if record not found.
        Post Data Models:
        Body: [{
            "field_id": "string",
            "instance_id": "string",
            "field_value": "string",
                }]
        """
        url = (
            self.study_url
            + f"/record/{record_id}/data-point-collection/survey-instance/{survey_instance_id}"
        )
        post_data = {"data": body, "common": {"change_reason": change_reason}}
        return self.sync_post(url, post_data)

    def update_survey_package_instance_data_record(
        self, record_id, survey_package_instance_id, body, change_reason, filled_on=None
    ):
        """Creates/updates a survey package instance.
        Returns None if record not found.
        Datetime is UTC time.
        Filled_on should be datetime or a string in the format: "yyyy-mm-dd hh:mm:ss
        Post Data Models:
        Body: [{
            "field_id": "string",
            "instance_id": "string",
            "field_value": "string",
                }]
        """
        url = (
            self.study_url + f"/record/{record_id}/data-point-collection/"
            f"survey-package-instance/{survey_package_instance_id}"
        )
        post_data = {"data": body, "common": {"change_reason": change_reason}}
        # Validate and format datetime
        if filled_on:
            if isinstance(filled_on, str):
                filled_on = datetime.strptime(filled_on, "%Y-%m-%d %H:%M:%S")
            post_data["all_fields_filled_on"] = filled_on.strftime("%Y-%m-%d %H:%M:%S")
        return self.sync_post(url, post_data)

    # EXPORT
    def export_study_data(
        self, exclude_empty_surveys=False, exclude_empty_reports=False
    ):
        """Returns a list of dicts containing all data in the study (study, surveys, reports)."""
        url = self.study_url + "/export/data"
        return self.sync_get(
            url=url,
            params={
                "exclude_empty_surveys": exclude_empty_surveys,
                "exclude_empty_reports": exclude_empty_reports,
            },
            timeout=httpx.Timeout(10.0, read=300),
        )["content"]

    def export_study_structure(self):
        """Returns a list of dicts containing the structure of the study."""
        url = self.study_url + "/export/structure"
        return self.sync_get(url=url, params={})["content"]

    def export_option_groups(self):
        """Returns a list of dicts containing all option groups in the study."""
        url = self.study_url + "/export/optiongroups"
        return self.sync_get(url=url, params={})["content"]

    # FIELDS
    def all_fields(self):
        """Returns a list of dicts of all fields."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field",
            data_name="fields",
            params={"include": "metadata,validations,optiongroup"},
        )

    def single_field(self, field_id):
        """Returns a dict of a single field.
        Returns None if field_id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field",
            data_id=field_id,
            params={"include": "metadata,validations,optiongroup"},
        )

    # FIELD DEPENDENCY
    def all_field_dependencies(self):
        """Returns a list of dicts of all field depencencies."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field-dependency", data_name="fieldDependencies"
        )

    def single_field_dependency(self, field_dependency_id):
        """Returns a single dict of a field dependency.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field-dependency", data_id=field_dependency_id
        )

    # FIELD OPTION GROUP
    def all_field_optiongroups(self):
        """Returns a list of dicts of all field option groups."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field-optiongroup", data_name="fieldOptionGroups"
        )

    def single_field_optiongroup(self, field_optiongroup_id):
        """Returns a single dict of a field optiongroup.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field-optiongroup", data_id=field_optiongroup_id
        )

    # FIELD VALIDATION
    def all_field_validations(self):
        """Returns a list of dicts of all field validations."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field-validation", data_name="fieldValidations"
        )

    def single_field_validation(self, field_validation_id):
        """Returns a single dict of a field validation.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field-validation", data_id=field_validation_id
        )

    # INSTITUTES
    def all_institutes(self):
        """Returns a list of dicts of all institutes."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/institute", data_name="institutes"
        )

    def single_institute(self, institute_id):
        """Returns a single dict of an institute.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/institute", data_id=institute_id)

    def create_institute(self, name, abbreviation, code, country_id):
        """Creates a institute for the study.
        Returns None if creation failed."""
        url = self.study_url + "/institute"
        body = [
            {
                "name": name,
                "abbreviation": abbreviation,
                "code": code,
                "country_id": country_id,
            }
        ]
        return self.sync_post(url, body)

    # METADATA
    def all_metadata(self):
        """Returns a list of dicts of all metadata."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/metadata", data_name="metadatas"
        )

    def single_metadata(self, metadata_id):
        """Returns a single dict of an metadata.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/metadata", data_id=metadata_id)

    # METADATATYPE
    def all_metadata_types(self):
        """Returns a list of dicts of all metadatatypes."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/metadatatype", data_name="metadatatypes"
        )

    def single_metadata_type(self, metadatatype_id):
        """Returns a single dict of an metadatatype.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/metadatatype", data_id=metadatatype_id
        )

    # PHASES
    def all_phases(self):
        """Returns a list of dicts of all phases."""
        return self.retrieve_all_data_by_endpoint(endpoint="/phase", data_name="phases")

    def single_phase(self, phase_id):
        """Returns a single dict of an phase.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/phase", data_id=phase_id)

    # QUERIES
    def all_queries(self):
        """Returns a list of dicts of all queries."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/query", data_name="queries"
        )

    def single_query(self, query_id):
        """Returns a single dict of an query.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/query", data_id=query_id)

    # RANDOMIZATION
    def single_randomization(self, record_id):
        """Gets randomisation details for a single record."""
        return self.retrieve_data_by_id(
            endpoint="/record", data_id=f"{record_id}/randomization"
        )

    def create_randomization(self, record_id):
        """Randomizes a single record."""
        url = self.study_url + f"/record/{record_id}/randomization"
        return self.sync_post(url=url, body={})

    # RECORD-DEVICE-TOKEN
    def single_token(self, record_id):
        """Gets the device token for a single record."""
        url = self.study_url + f"/record/{record_id}/device-token"
        return self.sync_get(url, params={})

    def create_token(self, record_id, token):
        """Creates a token for a record."""
        url = self.study_url + f"/record/{record_id}/device-token"
        return self.sync_post(url=url, body={"device_token": token})

    def update_token(self, record_id, token):
        """Updates a token for a record."""
        url = self.study_url + f"/record/{record_id}/device-token"
        return self.sync_patch(url=url, body={"device_token": token})

    def delete_token(self, record_id):
        """Deletes the token for a record."""
        url = self.study_url + f"/record/{record_id}/device-token"
        return self.sync_delete(url, params={})

    # RECORDS
    def all_records(self, institute_id=None, archived=None):
        """Returns a list of dicts of all records.
        Archived can be None (all records), 0 (unarchived records)
        or 1 (archived records)."""
        params = {}
        if institute_id is not None:
            params["institute"] = str(institute_id)
        if archived is not None:
            params["archived"] = str(archived)
        return self.retrieve_all_data_by_endpoint(
            endpoint="/record", data_name="records", params=params
        )

    def single_record(self, record_id):
        """Returns a dict of a record.
        Returns None when record not found."""
        return self.retrieve_data_by_id(endpoint="/record", data_id=record_id)

    def create_record(self, institute_id, email, record_id=None, ccr_patient_id=None):
        """Creates a record. Record_id is only necessary when id generation
        strategy is set to free text. Ccr_patient_id is an optional parameter.
        Returns None when record creation failed."""
        body = {
            "record_id": record_id,
            "ccr_record_id": ccr_patient_id,
            "institute_id": institute_id,
            "email_address": email,
        }
        url = self.study_url + "/record"
        return self.sync_post(url, body)

    # REPORTS
    def all_reports(self):
        """Returns a list of dicts of all reports."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/report", data_name="reports"
        )

    def single_report(self, report_id):
        """Returns a single dict of an report.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/report", data_id=report_id)

    # REPORT INSTANCES
    def all_report_instances(self, archived=0):
        """Returns a list of dicts of all non-archived report_instances.
        Supply argument archived=1 to also add archived report instances"""
        try:
            params = {"archived": archived}
            return self.retrieve_all_data_by_endpoint(
                endpoint="/report-instance", data_name="reportInstances", params=params
            )
        except HTTPStatusError as error:
            if error.response.json()["detail"] == "There are no report instances.":
                return []
            raise error from error

    def single_report_instance(self, report_instance_id):
        """Returns a single dict of an report_instance.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/report-instance", data_id=report_instance_id
        )

    def all_report_instances_record(self, record_id, archived=0):
        """Returns a list of dicts of all report_instances for record_id.
        Set archived to 1 to also retrieve archived report instances.
        Returns None if record not found."""
        formatted_endpoint = f"/record/{record_id}/report-instance"
        params = {"archived": archived}
        return self.retrieve_all_data_by_endpoint(
            endpoint=formatted_endpoint, data_name="reportInstances", params=params
        )

    def single_report_instance_record(self, record_id, report_instance_id):
        """Returns a dict containing the given report for record.
        Returns None if record or report not found."""
        formatted_endpoint = f"/record/{record_id}/report-instance"
        return self.retrieve_data_by_id(
            endpoint=formatted_endpoint, data_id=report_instance_id
        )

    def create_report_instance_record(
        self, record_id, report_id, report_name_custom, parent_id=None
    ):
        """Creates a report instance for a record.
        Returns None if creation failed."""
        url = self.study_url + f"/record/{record_id}/report-instance"
        body = {
            "report_id": report_id,
            "report_name_custom": report_name_custom,
            "parent_id": parent_id,
        }
        return self.sync_post(url, body)

    def create_multiple_report_instances_record(self, record_id, body):
        """Creates multiple report instances for a record.
        Body should be a list of dictionaries formatted according to:
        "report_id": report_id,
        "report_name_custom": report_name_custom,
        "parent_id": parent_id
        """
        data = {"data": body}
        url = self.study_url + f"/record/{record_id}/report-instance-collection"
        return self.sync_post(url, data)

    # REPORT-DATA-ENTRY
    def single_report_instance_all_fields_record(self, record_id, report_instance_id):
        """Returns a list of all data for a report for a record.
        Returns None if report not found for given id."""
        formatted_url = f"/record/{record_id}/data-point/report/{report_instance_id}"
        return self.retrieve_all_data_by_endpoint(
            endpoint=formatted_url, data_name="ReportDataPoints"
        )

    def single_report_instance_single_field_record(
        self, record_id, report_instance_id, field_id
    ):
        """Returns a data point for a report for a record.
        Returns None if report not found for given record or field not found
        for given report."""
        data_point = "/".join([report_instance_id, field_id])
        formatted_url = f"/record/{record_id}/data-point/report"
        return self.retrieve_data_by_id(endpoint=formatted_url, data_id=data_point)

    def update_report_instance_single_field_record(
        self,
        record_id,
        report_ins_id,
        field_id,
        change_reason,
        field_value=None,
        file=None,
    ):
        """Updates a report field value. Either field_value or file needs to be None.
        Returns None if data creation failed."""
        endpoint = f"/record/{record_id}/data-point/report/{report_ins_id}/{field_id}"
        url = self.study_url + endpoint
        body = {}

        if field_value is not None and file is not None:
            raise CastorException("You cannot both upload a field value and a file.")

        if field_value is not None:
            body = {
                "field_value": str(field_value),
                "change_reason": change_reason,
                "instance_id": report_ins_id,
            }

        elif file is not None:
            raise CastorException("File Uploading not implemented.")

        return self.sync_post(url, body)

    # REPORT-STEP
    def single_report_all_steps(self, report_id):
        """Returns a list of dicts of all steps of a single report.
        Returns None if report not found."""
        endpoint = f"/report/{report_id}/report-step"
        return self.retrieve_all_data_by_endpoint(
            endpoint=endpoint, data_name="report_steps"
        )

    def single_report_single_step(self, report_id, report_step_id):
        """Returns a single dict of a step of a report.
        Returns None if report or step not found."""
        endpoint = f"/report/{report_id}/report-step"
        return self.retrieve_data_by_id(endpoint=endpoint, data_id=report_step_id)

    # ROLE
    def all_roles(self):
        """Returns a list of dicts of all study roles."""
        return self.sync_get(url=self.study_url + "/role", params={})["_embedded"][
            "roles"
        ]

    def single_role(self, role_id):
        """Returns a single dict of a role in the study.
        Returns None if id not found.."""
        return self.retrieve_data_by_id(endpoint="/role", data_id=role_id)

    def create_role(self, name, description, permissions):
        """Creates a new role for the study.
        Permissions should be in the form of: {
                "add": bool,
                "view": bool,
                "edit": bool,
                "delete": bool,
                "lock": bool,
                "query": bool,
                "export": bool,
                "randomization_read": bool,
                "sign": bool,
                "email_addresses": bool,
                "randomization_write": bool,
                "sdv": bool,
                "survey_send": bool,
                "survey_view": bool
        }"""
        body = {"name": name, "description": description, "permissions": permissions}
        url = self.study_url + "/role"
        return self.sync_post(url=url, body=body)

    # STEP
    def all_steps(self):
        """Returns a list of dicts of all study steps."""
        return self.retrieve_all_data_by_endpoint(endpoint="/step", data_name="steps")

    def single_step(self, step_id):
        """Returns a single dict of a step in the study.
        Returns None if id not found.."""
        return self.retrieve_data_by_id(endpoint="/step", data_id=step_id)

    # STUDY
    def all_studies(self):
        """Returns a list of dicts of studies you have access to."""
        endpoint = "/study"
        all_studies = self.retrieve_general_data(
            endpoint, embedded=True, data_id="study"
        )
        return all_studies

    def single_study(self, study_id):
        """Returns a dict of a single study.
        Returns None if study not found or not authorized to view study."""
        endpoint = f"/study/{study_id}"
        return self.retrieve_general_data(endpoint)

    def all_users_study(self, study_id):
        """Returns a list of dicts of users that have access to this study.
        Returns None if study not found or not authorized to view study."""
        endpoint = f"/study/{study_id}/user"
        all_users = self.retrieve_general_data(
            endpoint, embedded=True, data_id="studyUsers"
        )
        return all_users

    def single_user_study(self, study_id, user_id):
        """Returns a user for given study.
        Returns None if study/user not found or not authorized to view study.
        """
        endpoint = f"/study/{study_id}/user/{user_id}"
        return self.retrieve_general_data(endpoint)

    def invite_user_study(
        self,
        study_id,
        institute_id,
        email,
        message,
        manage_permissions=None,
        institute_permissions=None,
    ):
        """Invites user with email to the study linked to institute_id."""
        url = self.base_url + f"/study/{study_id}/user"
        body = {
            "institute_id": institute_id,
            "email": email,
            "message": message,
            "manage_permission": manage_permissions,
            "institute_permissions": institute_permissions,
        }
        return self.sync_post(url, body)

    # STUDY-DATA-ENTRY
    def all_study_fields_record(self, record_id):
        """Returns a list of all study fields of a record.
        Returns None if record not found."""
        endpoint = f"/record/{record_id}/data-point/study"
        return self.retrieve_all_data_by_endpoint(endpoint, data_name="StudyDataPoints")

    def single_study_field_record(self, record_id, field_id):
        """Returns the value for a single field for a record in the study.
        Returns None if record or field not found."""
        endpoint = f"/record/{record_id}/data-point/study"
        return self.retrieve_data_by_id(endpoint, data_id=field_id)

    def update_single_study_field_record(
        self, record_id, field_id, change_reason, field_value=None, file=None
    ):
        """Update a data point for a record.
        Returns None if target not found."""
        url = self.study_url + f"/record/{record_id}/data-point/study/{field_id}"
        body = {}
        if field_value is not None and file is not None:
            raise CastorException("You cannot both upload a field value and a file.")

        if field_value is not None:
            body = {
                "field_value": str(field_value),
                "change_reason": change_reason,
            }

        elif file is not None:
            raise CastorException("File Uploading not implemented.")
        return self.sync_post(url, body)

    # STATISTICS
    def statistics(self):
        """Returns statistics for the linked study"""
        endpoint = "statistics"
        return self.retrieve_data_by_id("", endpoint)

    # SURVEY
    def all_surveys(self):
        """Returns a list of dicts of all available surveys."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/survey", data_name="surveys"
        )

    def single_survey(self, survey_id):
        """Returns a single dict of a survey in the study.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/survey", data_id=survey_id)

    def all_survey_packages(self):
        """Returns a list of dicts of all available survey packages."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/surveypackage", data_name="survey_packages"
        )

    def single_survey_package(self, survey_package_id):
        """Returns a single dict of a survey package in the study.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/surveypackage", data_id=survey_package_id
        )

    def all_survey_package_instances(
        self,
        record_id=None,
        ccr_patient_id=None,
        finished_on=None,
        finished_on_gt=None,
        finished_on_gte=None,
        finished_on_lt=None,
        finished_on_lte=None,
    ):
        """Returns a list of dicts of all available survey packages. Filterable."""
        endpoint = "/surveypackageinstance"
        dataname = "surveypackageinstance"
        if record_id and ccr_patient_id:
            raise CastorException("Cannot supply both record_id and ccr_patient_id")
        params = {
            "record_id": record_id,
            "ccr_patient_id": ccr_patient_id,
            "finished_on": finished_on,
            "finished_on[gt]": finished_on_gt,
            "finished_on[gte]": finished_on_gte,
            "finished_on[lt]": finished_on_lt,
            "finished_on[lte]": finished_on_lte,
        }
        # Drop empty params
        params = {key: value for key, value in params.items() if value is not None}
        data = self.retrieve_all_data_by_endpoint(
            endpoint=endpoint, data_name=dataname, params=params
        )
        return data

    def single_survey_package_instance(self, survey_package_instance_id):
        """Returns a single dict of a survey package in the study.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/surveypackageinstance", data_id=survey_package_instance_id
        )

    def create_survey_package_instance(
        self,
        survey_package_id,
        record_id,
        email_address,
        ccr_patient_id=None,
        package_invitation_subject=None,
        package_invitation=None,
        auto_send=None,
        auto_lock_on_finish=None,
    ):
        """Create a survey package.
        Arguments marked with None are non-obligatory."""
        url = self.study_url + "/surveypackageinstance"
        body = {
            "survey_package_id": survey_package_id,
            "record_id": record_id,
            "ccr_patient_id": ccr_patient_id,
            "email_address": email_address,
            "package_invitation_subject": package_invitation_subject,
            "package_invitation": package_invitation,
            "auto_send": auto_send,
            "auto_lock_on_finish": auto_lock_on_finish,
        }
        return self.sync_post(url, body)

    def lock_unlock_survey_package_instance(self, survey_package_instance_id, status):
        """Lock/unlock survey package."""
        url = self.study_url + f"/surveypackageinstance/{survey_package_instance_id}"
        body = {
            "locked": status,
        }
        return self.sync_patch(url, body)

    def update_start_time_survey_package_instance(
        self,
        record_id: str,
        survey_package_instance_id: str,
        date_time: Union[str, datetime],
    ):
        """Updates start time of survey package. Datetime is UTC time.
        Datetime should be datetime or string in the format: "yyyy-mm-dd hh:mm:ss"""
        url = (
            self.study_url
            + f"/record/{record_id}/surveypackageinstance/{survey_package_instance_id}"
        )
        if isinstance(date_time, str):
            date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        body = {
            "started_on": date_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return self.sync_patch(url, body)

    # SURVEY-DATA-ENTRY
    def single_survey_instance_all_fields_record(self, record_id, survey_instance_id):
        """Retrieves a list of fields with data for a single survey.
        Returns None if record or survey not found."""
        endpoint = f"/record/{record_id}/data-point/survey/{survey_instance_id}"
        return self.retrieve_all_data_by_endpoint(
            endpoint, data_name="SurveyDataPoints"
        )

    def single_survey_instance_single_field_record(
        self, record_id, survey_instance_id, field_id
    ):
        """Retrieves a single field with data for the given survey.
        Returns None if record, survey or field not found."""
        endpoint = f"/record/{record_id}/data-point/survey/{survey_instance_id}"
        return self.retrieve_data_by_id(endpoint, data_id=field_id)

    def update_survey_instance_single_field_record(
        self, record_id, survey_instance_id, field_id, field_value, change_reason
    ):
        """Update a field result for a survey (package) instance.
        Returns None if survey not found"""
        url = (
            self.study_url
            + f"/record/{record_id}/data-point/survey/{survey_instance_id}/{field_id}"
        )
        body = {
            "field_value": str(field_value),
            "change_reason": change_reason,
            "instance_id": survey_instance_id,
            # "upload_file": None,
        }
        return self.sync_post(url, body)

    # SURVEY-STEP
    def single_survey_all_steps(self, survey_id):
        """Retrieves a list of dicts of steps for a single survey.
        Returns None if survey not found."""
        endpoint = f"/survey/{survey_id}/survey-step"
        return self.retrieve_all_data_by_endpoint(endpoint, data_name="survey_steps")

    def single_survey_single_step(self, survey_id, survey_step_id):
        """Retrieves a dict of a single survey step.
        Returns None if survey or step not found."""
        endpoint = f"/survey/{survey_id}/survey-step"
        return self.retrieve_data_by_id(endpoint, data_id=survey_step_id)

    # USER
    def all_users(self):
        """Retrieves list of users that current user is authorized to see."""
        endpoint = "/user"
        return self.retrieve_general_data(endpoint, embedded=True, data_id="user")

    def single_user(self, user_id):
        """Retrieves a single user by ID."""
        endpoint = f"/user/{user_id}"
        return self.retrieve_general_data(endpoint)

    # RECORD PROGRESS
    def record_progress(self):
        """Returns progress of all records."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/record-progress/steps", data_name="records"
        )

    # VERIFICATIONS
    def verifications(
        self,
        record_id: Optional[str] = None,
        date_from: Union[str, datetime, None] = None,
        date_to: Union[str, datetime, None] = None,
        verification_types: Optional[List] = None,
        entity_types: Optional[List] = None,
    ):
        """Returns a dict of the verifications.
        date_from and date_to need to datetime or string formatted as yyyy-mm-dd."""
        if isinstance(date_from, str):
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
        if isinstance(date_to, str):
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        params = {
            key: value
            for key, value in {
                "record_id": record_id,
                "date_from": date_from.strftime("%Y-%m-%d") if date_from else None,
                "date_to": date_to.strftime("%Y-%m-%d") if date_to else None,
            }.items()
            if value
        }
        if verification_types:
            params["verification_type"] = ",".join(verification_types)
        if entity_types:
            params["entity_type"] = ",".join(entity_types)
        return self.retrieve_all_data_by_endpoint(
            endpoint="/verification", data_name="verifications", params=params
        )

    # HELPER FUNCTIONS
    def request_auth_token(self, client_id, client_secret):
        """Request an authentication token from Castor EDC for given client."""
        auth_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        response = self.client.post(url=self.auth_url, content=json.dumps(auth_data))
        response.raise_for_status()
        content = response.json()
        return content["access_token"]

    def retrieve_general_data(self, endpoint, embedded=False, data_id=""):
        """Helper function for retrieving data from an endpoint.
        Unpacks data if embedded in the response."""
        url = self.base_url + endpoint
        params = {}
        response = self.sync_get(url=url, params=params)
        if embedded:
            data = response["_embedded"][data_id]
        else:
            data = response
        return data

    def retrieve_data_points(self, endpoint):
        """Retrieves data point with data_id.
        Returns None if data_id is not found at given endpoint."""
        url = self.study_url + endpoint
        params = {}
        data = self.sync_get(url=url, params=params)
        return data["_embedded"]["items"]

    def retrieve_data_by_id(self, endpoint, data_id, params=None):
        """Retrieves data point with data_id.
        Returns None if data_id is not found at given endpoint."""
        url = self.study_url + endpoint + f"/{data_id}"
        if params is None:
            params = {}
        data = self.sync_get(url=url, params=params)
        return data

    def retrieve_all_data_by_endpoint(self, endpoint, data_name, params=None):
        """Retrieves all data on endpoint.
        data_name is that which holds data within ['_embedded'] (ex: 'fields')
        params is a dict of extra information to be sent."""
        url = self.study_url + endpoint
        if params is None:
            params = {}
        return self.retrieve_multiple_pages(url=url, params=params, data_name=data_name)

    # Functions to retrieve paginated data with async requests
    def retrieve_multiple_pages(self, url, params, data_name):
        """Helper function to gather all data when there are multiple pages.
        data_name is that which holds data within ['_embedded'] (ex: 'fields')
        """
        # Retrieve the first page to see the size
        first_response = self.retrieve_single_page(url=url, params=params.copy())
        pages = first_response["page_count"] + 1
        rest_response = self.retrieve_rest_of_pages(url=url, params=params, pages=pages)
        data = list(
            chain.from_iterable(
                [
                    response["_embedded"][data_name]
                    for response in [first_response] + rest_response
                ]
            )
        )
        return data

    def retrieve_single_page(self, url, params):
        """Helper function to query a single page and return the data from that page."""
        if params is None:
            params = {"page": "1", "page_size": "1000"}
        else:
            params["page"] = "1"
            params["page_size"] = "1000"
        response = self.sync_get(url=url, params=params)
        return response

    def retrieve_rest_of_pages(self, url, params, pages):
        """Helper function to gather all data when there are multiple pages.
        data_name is that which holds data within ['_embedded'] (ex: 'fields')
        """
        if params is None:
            params = [
                {"page": str(page), "page_size": "1000"} for page in range(2, pages)
            ]
        else:
            params = [
                {"page": str(page), "page_size": "1000", **params}
                for page in range(2, pages)
            ]
        try:
            # Test if there is a running event loop
            # If there is, we can't use async code
            # Solution for IPython consoles (Jupiter Notebooks, Spyder3)
            asyncio.get_running_loop()
            responses = [self.sync_get(url, param) for param in tqdm(params)]
        except RuntimeError:
            # No running event loop, free to use async code
            responses = asyncio.run(self.async_get(url=url, params=params))
            responses = [self.handle_response(response) for response in responses]

        return responses

    def request_size(self, endpoint, base=False):
        """Helper function for tests to determine how many items there are per given endpoint"""
        if not base:
            url = self.study_url + endpoint
        else:
            url = self.base_url + endpoint
        response = self.sync_get(url=url, params={})
        return response["total_items"]

    # Synchronous API Interaction
    def sync_get(self, url: str, params: dict, timeout=None) -> dict:
        """Synchronous querying of Castor API with a single get requests."""
        if timeout:
            response = self.client.get(url=url, params=params, timeout=timeout)
        else:
            response = self.client.get(url=url, params=params)
        return self.handle_response(response)

    def sync_post(self, url, body):
        """Helper function to post body to url."""
        response = self.client.post(url=url, json=body)
        response.raise_for_status()
        return response.json()

    def sync_patch(self, url, body):
        """Helper function to patch body to url."""
        response = self.client.patch(url=url, json=body)
        response.raise_for_status()
        return response.json()

    def sync_delete(self, url, params: dict):
        """Helper function to send delete to url."""
        response = self.client.delete(url=url, params=params)
        response.raise_for_status()
        return response.json()

    # Asynchronous API Interaction
    async def async_get(self, url: str, params: list) -> list:
        """Queries the Castor EDC API on given url with parameters params.
        Queries the database once for each parameter dict in the params list.
        Returns a list of responses.

        :param url: the urls for the request
        :param params: a list of dicts of the parameters to be send with the request
        """
        # Split list to handle error when len(tasks) > max_connections
        chunks = [
            params[x : x + self.max_connections]
            for x in range(0, len(params), self.max_connections)
        ]
        responses = []
        for idx, chunk in enumerate(chunks):
            async with httpx.AsyncClient(
                headers=self.headers, timeout=self.timeout, limits=self.limits
            ) as client:
                tasks = [client.get(url=url, params=param) for param in chunk]
                temp_responses = [
                    await response
                    for response in tqdm(
                        asyncio.as_completed(tasks),
                        total=len(tasks),
                        desc=f"Async Downloading {idx + 1}/{len(chunks)}",
                    )
                ]
                responses = responses + temp_responses
        return responses

    @staticmethod
    def handle_response(response: httpx.Response) -> dict:
        """Reads response and handles errors."""
        response.raise_for_status()
        content_type = response.headers.get("content-type")
        if "json" in content_type:
            data = response.json()
        elif "csv" in content_type:
            content_decoded = response.content.decode()
            content_csv = list(
                csv.DictReader(content_decoded.splitlines(), delimiter=";")
            )
            data = {"content": content_csv}
        else:
            raise CastorException(f"{content_type} not supported")
        return data

    @property
    def headers(self):
        """Return the headers that will be sent with each request"""
        return self.client.headers
