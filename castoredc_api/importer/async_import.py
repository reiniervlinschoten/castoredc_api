"""Module to import data (synchronous) to Castor EDC using the API"""

import pathlib
import typing
import asyncio
from datetime import datetime
import pandas as pd

from castoredc_api.importer.async_helpers import (
    async_update_survey_data,
    async_update_study_data,
    async_update_report_data,
)
from castoredc_api.importer.helpers import create_feedback

if typing.TYPE_CHECKING:
    from castoredc_api import CastorStudy


def upload_study_async(
    castorized_dataframe: pd.DataFrame,
    common: dict,
    upload_datetime: str,
    study: "CastorStudy",
) -> dict:
    """Uploads study data to the study asynchronously."""
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

    # Upload data
    imported = asyncio.run(async_update_study_data(data, study))
    # Create feedback for user
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
    change_reason: str,
) -> dict:
    """Uploads survey data to the study."""
    data = []
    # Prepare data for each row
    for row in castorized_dataframe.to_dict("records"):
        data.append({"row": row, "package_id": package_id, "email": email})
    # Upload data
    imported = asyncio.run(async_update_survey_data(data, study, change_reason))
    # Save output
    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    # Create feedback for the user
    feedback = create_feedback(imported)
    return feedback


def upload_report_async(
    castorized_dataframe: pd.DataFrame,
    common: dict,
    upload_datetime: str,
    study: "CastorStudy",
    report_id: str,
) -> dict:
    """Uploads report data to the study asynchronously."""
    data = []
    # Prepare data for upload, can't have identical names
    for count, row in enumerate(castorized_dataframe.to_dict("records")):
        data.append(
            {
                "row": row,
                "report_id": report_id,
                "upload_datetime": upload_datetime,
                "report_name": f"{upload_datetime} - {count}",
                "common": common,
            }
        )
    # Upload data for the user
    imported = asyncio.run(async_update_report_data(data, study))

    # Save output
    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    # Create feedback for the user
    feedback = create_feedback(imported)
    return feedback
