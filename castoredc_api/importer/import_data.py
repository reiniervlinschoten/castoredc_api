"""Module to import data to Castor EDC using the API"""
import sys
from datetime import datetime
import typing
import pathlib
import pandas as pd

from httpx import HTTPStatusError
from tqdm import tqdm

from castoredc_api import CastorException
from castoredc_api.importer.helpers import create_upload, format_feedback, handle_httpstatuserror, handle_failed_upload, \
    create_feedback, handle_response, create_survey_body, create_report_body

if typing.TYPE_CHECKING:
    from castoredc_api import CastorStudy


def import_data(
        data_source_path: str,
        column_link_path: str,
        study: "CastorStudy",
        label_data: bool,
        target: str,
        target_name: typing.Optional[str] = None,
        email: typing.Optional[str] = None,
        translation_path: typing.Optional[str] = None,
        merge_path: typing.Optional[str] = None,
        format_options=None,
) -> dict:
    """Imports data from data_source_path to study with configuration options.
    Returns a dict with successful and failed uploads."""
    # Set configuration options
    configuration = {
        "date": "%d-%m-%Y",
        "datetime": "%d-%m-%Y;%H:%M",
        "time": "%H:%M",
    }
    if format_options:
        configuration.update(format_options)

    # Map the structure of your study locally
    study.map_structure()

    # Prepare output directory
    pathlib.Path(pathlib.Path.cwd(), "output").mkdir(parents=True, exist_ok=True)

    # Create the castorized dataframe
    castorized_dataframe = create_upload(
        path_to_upload=data_source_path,
        path_to_col_link=column_link_path,
        path_to_translation=translation_path,
        path_to_merge=merge_path,
        label_data=label_data,
        study=study,
        format_options=configuration,
    )
    # Tests if Error is anywhere in the dataframe
    if "Error" in castorized_dataframe.to_string():
        castorized_dataframe.to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                + "error_before_upload.csv",
            ),
            index=False,
        )
        raise CastorException(
            "Non-viable data found in dataset to be imported. See output folder for details"
        )
    # Upload the data
    return upload_data(castorized_dataframe, study, target, target_name, email)


def upload_data(
        castorized_dataframe: pd.DataFrame,
        study: "CastorStudy",
        target: str,
        target_name: typing.Optional[str],
        email: typing.Optional[str],
) -> dict:
    """Uploads each row from the castorized dataframe as a new form"""
    # Shared Data
    upload_datetime = datetime.now().strftime("%Y%m%d %H%M%S")
    common = {
        "change_reason": f"api_upload_{target}_{upload_datetime}",
        "confirmed_changes": True,
    }

    if target == "Study":
        upload = upload_study(castorized_dataframe, common, upload_datetime, study)
    elif target == "Survey":
        target_form = next(
            (
                form
                for form in study.client.all_survey_packages()
                if form["name"] == target_name
            ),
            None,
        )
        upload = upload_survey(castorized_dataframe, study, target_form["id"], email)
    elif target == "Report":
        target_form = study.get_single_form_name(target_name)
        upload = upload_report(
            castorized_dataframe,
            common,
            upload_datetime,
            study,
            target_form.form_id,
        )
    else:
        raise CastorException(
            f"{target} is not a valid target. Use Study/Report/Survey."
        )
    return upload


def upload_study(
        castorized_dataframe: pd.DataFrame,
        common: dict,
        upload_datetime: str,
        study: "CastorStudy",
) -> dict:
    """Uploads study data to the study."""
    imported = []

    for row in tqdm(
            castorized_dataframe.to_dict("records"), "Uploading Data", file=sys.stdout
    ):
        body = [
            {
                "field_id": study.get_single_field(field).field_id,
                "field_value": row[field],
                "change_reason": f"api_upload_Study_{upload_datetime}",
                "confirmed_changes": True,
            }
            for field in row
            # Skip record_id and empty fields
            if (field != "record_id" and row[field] is not None)
        ]

        # Upload the data
        imported = upload_study_data(body, study, common, imported, row)

    # Output log of upload
    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    feedback = create_feedback(imported)
    return feedback


def upload_study_data(
        body: list, study: "CastorStudy", common: dict, imported: list, row: "dict"
):
    """Uploads a single row of study data."""
    try:
        # Upload single row
        feedback_row = study.client.update_study_data_record(
            record_id=row["record_id"], common=common, body=body
        )
        # Format feedback
        formatted_feedback_row = format_feedback(feedback_row, study)
        # Add successes and failures
        row["success"] = formatted_feedback_row["success"]
        row["failed"] = formatted_feedback_row["failed"]
        # Add to the dataset
        imported.append(row)
        if len(formatted_feedback_row["failed"]) > 0:
            handle_failed_upload(formatted_feedback_row, imported, row)
    except HTTPStatusError as error:
        handle_httpstatuserror(error, imported, row)
    return imported


def upload_survey(
        castorized_dataframe: pd.DataFrame,
        study: "CastorStudy",
        package_id: str,
        email: str,
) -> dict:
    """Uploads survey data to the study."""
    imported = []

    for row in tqdm(
            castorized_dataframe.to_dict("records"), "Uploading Data", file=sys.stdout
    ):
        instance = create_survey_package_instance(
            study, imported, package_id, row, email
        )
        # Create body to send
        body = create_survey_body(instance, row, study)
        # Upload the data
        imported = upload_survey_data(body, study, imported, instance, row)

    # Save output
    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    feedback = create_feedback(imported)
    return feedback


def upload_survey_data(
        body: list, study: "CastorStudy", imported: list, instance: dict, row: dict
) -> dict:
    """Tries to upload the survey data."""
    try:
        # Upload single row
        response = study.client.update_survey_package_instance_data_record(
            record_id=row["record_id"],
            survey_package_instance_id=instance["id"],
            body=body,
        )
        imported = handle_response(response, imported, row, study)
    except HTTPStatusError as error:
        handle_httpstatuserror(error, imported, row)
    return imported


def create_survey_package_instance(
        study: "CastorStudy", imported: list, package_id: str, row: dict, email: str
) -> dict:
    """Tries to create a new survey package instance of package and for record."""
    try:
        instance = study.client.create_survey_package_instance(
            survey_package_id=package_id,
            record_id=row["record_id"],
            email_address=email,
            auto_send=False,
        )
        return instance
    except HTTPStatusError as error:
        handle_httpstatuserror(error, imported, row)


def upload_report(
        castorized_dataframe: pd.DataFrame,
        common: dict,
        upload_datetime: str,
        study: "CastorStudy",
        package_id: str,
) -> dict:
    """Uploads report data to the study."""
    imported = []
    for row in tqdm(
            castorized_dataframe.to_dict("records"), "Uploading Data", file=sys.stdout
    ):
        # Create a report instance
        instance = create_report_instance(
            study, imported, package_id, row
        )
        # Create the report body
        body = create_report_body(instance, row, study, upload_datetime)

        # Upload the data
        imported = upload_report_data(
            body, study, imported, instance, row, common
        )
    # Save output
        pd.DataFrame(imported).to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
            ),
            index=False,
        )
    feedback = create_feedback(imported)
    return feedback


def upload_report_data(
        body: list,
        study: "CastorStudy",
        imported: list,
        instance: dict,
        row: dict,
        common: dict,
) -> dict:
    """Tries to upload the survey data."""
    try:
        response = study.client.update_report_data_record(
            record_id=row["record_id"],
            report_id=instance["id"],
            common=common,
            body=body,
        )
        imported = handle_response(response, imported, row, study)
    except HTTPStatusError as error:
        handle_httpstatuserror(error, imported, row)
    return imported


def create_report_instance(
        study: "CastorStudy",
        imported: list,
        package_id: str,
        row: dict
) -> list:
    """Creates a new report instance for record."""
    try:
        record = row["record_id"]
        instance = study.client.create_report_instance_record(
            record_id=record, report_id=package_id, report_name_custom=f"{record}-api_upload_Report_{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
        )
    except HTTPStatusError as error:
        handle_httpstatuserror(error, imported, row)
    return instance
