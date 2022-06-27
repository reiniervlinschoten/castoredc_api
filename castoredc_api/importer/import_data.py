"""Module to import data to Castor EDC using the API"""
from datetime import datetime
import typing
import pathlib

import pandas as pd

from castoredc_api import CastorException
from castoredc_api.importer.async_import import (
    upload_survey_async,
    upload_report_async,
    upload_study_async,
)
from castoredc_api.importer.helpers import create_upload
from castoredc_api.importer.sync_import import (
    upload_survey,
    upload_study,
    upload_report,
)

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
    use_async=False,
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
        target=target,
        target_name=target_name,
    )

    # Tests if Error is anywhere in the dataframe
    if (
        "Error"
        in castorized_dataframe.to_string()  # pylint: disable=unsupported-membership-test
    ):
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
    upload = upload_data(
        castorized_dataframe, study, target, target_name, email, use_async
    )

    # Print results
    print(
        f"Success: {sum(len(row['success']) for key, item in upload.items() for row in item)} \n"
        f"Failure: {sum(len(row['failed']) for key, item in upload.items() for row in item)} \n"
        f"Error: {sum(len(row['error']) for key, item in upload.items() for row in item)}"
    )

    return upload


def upload_data(
    castorized_dataframe: pd.DataFrame,
    study: "CastorStudy",
    target: str,
    target_name: typing.Optional[str],
    email: typing.Optional[str],
    use_async: bool = False,
) -> dict:
    """Uploads each row from the castorized dataframe as a new form"""
    # Shared Data
    upload_datetime = datetime.now().strftime("%Y%m%d %H%M%S")
    common = {
        "change_reason": f"api_upload_{target}_{upload_datetime}",
        "confirmed_changes": True,
    }

    if target == "Study":
        if use_async:
            upload = upload_study_async(
                castorized_dataframe, common, upload_datetime, study
            )
        else:
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
        if use_async:
            upload = upload_survey_async(
                castorized_dataframe,
                study,
                target_form["id"],
                email,
                f"api_upload_{target}_{upload_datetime}",
            )
        else:
            upload = upload_survey(
                castorized_dataframe,
                study,
                target_form["id"],
                email,
                f"api_upload_{target}_{upload_datetime}",
            )
    elif target == "Report":
        target_form = study.get_single_form_name(target_name)
        if use_async:
            upload = upload_report_async(
                castorized_dataframe,
                common,
                upload_datetime,
                study,
                target_form.form_id,
            )
        else:
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
