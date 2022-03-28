"""Module to import data (synchronous) to Castor EDC using the API"""

import pathlib
import typing
from datetime import datetime
from json import JSONDecodeError

import pandas as pd
from httpx import HTTPStatusError, RequestError
from tqdm import tqdm

from castoredc_api.importer.helpers import (
    format_feedback,
    handle_http_error,
    handle_failed_upload,
    create_feedback,
    handle_response,
    create_survey_body,
    create_report_body,
)

if typing.TYPE_CHECKING:
    from castoredc_api import CastorStudy


def upload_study(
    castorized_dataframe: pd.DataFrame,
    common: dict,
    upload_datetime: str,
    study: "CastorStudy",
) -> dict:
    """Uploads study data to the study."""
    imported = []

    for row in tqdm(castorized_dataframe.to_dict("records"), "Uploading Data"):
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
    except (HTTPStatusError, RequestError, JSONDecodeError) as error:
        handle_http_error(error, imported, row)
    return imported


def upload_survey(
    castorized_dataframe: pd.DataFrame,
    study: "CastorStudy",
    package_id: str,
    email: str,
    change_reason: str,
) -> dict:
    """Uploads survey data to the study."""
    imported = []

    for row in tqdm(castorized_dataframe.to_dict("records"), "Uploading Data"):
        instance = create_survey_package_instance(
            study, imported, package_id, row, email
        )
        # Create body to send
        body = create_survey_body(instance, row, study)
        # Upload the data
        imported = upload_survey_data(
            body, study, imported, instance, row, change_reason
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


def upload_survey_data(
    body: list,
    study: "CastorStudy",
    imported: list,
    instance: dict,
    row: dict,
    change_reason: str,
) -> dict:
    """Tries to upload the survey data."""
    try:
        # Upload single row
        response = study.client.update_survey_package_instance_data_record(
            record_id=row["record_id"],
            survey_package_instance_id=instance["id"],
            body=body,
            change_reason=change_reason,
        )
        imported = handle_response(response, imported, row, study)
    except (HTTPStatusError, RequestError, JSONDecodeError) as error:
        handle_http_error(error, imported, row)
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
    except (HTTPStatusError, RequestError, JSONDecodeError) as error:
        handle_http_error(error, imported, row)
    return instance


def upload_report(
    castorized_dataframe: pd.DataFrame,
    common: dict,
    upload_datetime: str,
    study: "CastorStudy",
    package_id: str,
) -> dict:
    """Uploads report data to the study."""
    imported = []
    for row in tqdm(castorized_dataframe.to_dict("records"), "Uploading Data"):
        # Create a report instance
        instance = create_report_instance(study, imported, package_id, row)
        # Create the report body
        body = create_report_body(instance, row, study, upload_datetime)

        # Upload the data
        imported = upload_report_data(body, study, imported, instance, row, common)
        # Save output
        pd.DataFrame(imported).to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                + "successful_upload.csv",
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
    except (HTTPStatusError, RequestError, JSONDecodeError) as error:
        handle_http_error(error, imported, row)
    return imported


def create_report_instance(
    study: "CastorStudy", imported: list, package_id: str, row: dict
) -> list:
    """Creates a new report instance for record."""
    try:
        record = row["record_id"]
        instance = study.client.create_report_instance_record(
            record_id=record,
            report_id=package_id,
            report_name_custom=f"{record}-api_upload_Report_"
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}",
        )
    except (HTTPStatusError, RequestError, JSONDecodeError) as error:
        handle_http_error(error, imported, row)
    return instance
