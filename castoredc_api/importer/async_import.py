"""Module to import data (synchronous) to Castor EDC using the API"""

import pathlib
import sys
import typing
import asyncio
from datetime import datetime
import pandas as pd
from httpx import HTTPStatusError
from tqdm import tqdm

from castoredc_api import CastorException
from castoredc_api.importer.async_helpers import (
    async_update_survey_data,
    async_update_study_data,
)
from castoredc_api.importer.helpers import (
    handle_httpstatuserror,
    create_feedback,
    handle_response,
    create_report_body,
)

if typing.TYPE_CHECKING:
    from castoredc_api import CastorStudy


def upload_data_async(
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
        upload = upload_study_async(
            castorized_dataframe, common, upload_datetime, study
        )
    elif target == "Survey":
        target_form = next(
            (
                form
                for form in study.client.all_survey_packages()
                if form["name"] == target_name
            ),
            None,
        )
        upload = upload_survey_async(
            castorized_dataframe, study, target_form["id"], email
        )
    elif target == "Report":
        target_form = study.get_single_form_name(target_name)
        upload = upload_report_async(
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


def upload_study_async(
    castorized_dataframe: pd.DataFrame,
    common: dict,
    upload_datetime: str,
    study: "CastorStudy",
) -> dict:
    """Uploads study data to the study."""
    data = []

    # Prepare data for async post
    for row in castorized_dataframe.to_dict("records"):
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
        data.append({"body": body, "common": common, "row": row})

    imported = asyncio.run(async_update_study_data(data, study))
    feedback = create_feedback(imported)
    # Output log of upload
    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    return feedback


def upload_survey_async(
    castorized_dataframe: pd.DataFrame,
    study: "CastorStudy",
    package_id: str,
    email: str,
) -> dict:
    """Uploads survey data to the study."""
    data = []
    for row in castorized_dataframe.to_dict("records"):
        data.append({"row": row, "package_id": package_id, "email": email})
    imported = asyncio.run(async_update_survey_data(data, study))

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
    except HTTPStatusError as error:
        handle_httpstatuserror(error, imported, row)
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
    except HTTPStatusError as error:
        handle_httpstatuserror(error, imported, row)
    return instance
