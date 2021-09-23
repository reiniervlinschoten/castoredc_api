"""Module to import data to Castor EDC using the API"""
from datetime import datetime
import typing
import pathlib
import pandas as pd

from httpx import HTTPStatusError
from tqdm import tqdm

from castoredc_api import CastorException
from castoredc_api.importer.helpers import create_upload, update_feedback

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
) -> dict:
    """Imports data from data_source_path to study with configuration options."""
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
    feedback_total = {}
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
        feedback_row = upload_study_data(body, study, common, imported, row)
        try:
            feedback_total = update_feedback(feedback_row, feedback_total, row, study)
        except CastorException as error:
            pd.DataFrame(imported).to_csv(
                pathlib.Path(
                    pathlib.Path.cwd(),
                    "output",
                    f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                    + "error_during_upload.csv",
                ),
                index=False,
            )
            raise CastorException(
                str(error)
                + " caused at "
                + str(row)
                + ".\n See output folder for successful imports"
            ) from error

    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    return feedback_total


def upload_study_data(
    body: dict, study: "CastorStudy", common: dict, imported: list, row: "dict"
):
    """Uploads a single row of study data."""
    try:
        feedback_row = study.client.update_study_data_record(
            record_id=row["record_id"], common=common, body=body
        )
        imported.append(row)
    except HTTPStatusError as error:
        pd.DataFrame(imported).to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                + "error_during_upload.csv",
            ),
            index=False,
        )
        raise CastorException(
            str(error)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from error
    return feedback_row


def upload_survey(
    castorized_dataframe: pd.DataFrame,
    study: "CastorStudy",
    package_id: str,
    email: str,
) -> dict:
    """Uploads survey data to the study."""
    feedback_total = {}
    imported = []

    for row in tqdm(castorized_dataframe.to_dict("records"), "Uploading Data"):
        instance = create_survey_package_instance(
            study, imported, package_id, row, email
        )

        # Create body to send
        body = [
            {
                "field_id": study.get_single_field(field).field_id,
                "instance_id": instance["id"],
                "field_value": row[field],
            }
            for field in row
            # Skip record_id and empty fields
            if (field != "record_id" and row[field] is not None)
        ]

        # Upload the data
        feedback_row = upload_survey_data(body, study, imported, instance, row)
        try:
            feedback_total = update_feedback(feedback_row, feedback_total, row, study)
        except CastorException as error:
            pd.DataFrame(imported).to_csv(
                pathlib.Path(
                    pathlib.Path.cwd(),
                    "output",
                    f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                    + "error_during_upload.csv",
                ),
                index=False,
            )
            raise CastorException(
                str(error)
                + " caused at "
                + str(row)
                + ".\n See output folder for successful imports"
            ) from error

    # Save output
    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    return feedback_total


def upload_survey_data(
    body: list, study: "CastorStudy", imported: list, instance: dict, row: dict
) -> dict:
    """Tries to upload the survey data."""
    try:
        feedback_row = study.client.update_survey_package_instance_data_record(
            record_id=row["record_id"],
            survey_package_instance_id=instance["id"],
            body=body,
        )
        imported.append(row)
    except HTTPStatusError as error:
        pd.DataFrame(imported).to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                + "error_during_upload.csv",
            ),
            index=False,
        )
        raise CastorException(
            str(error)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from error
    return feedback_row


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
    except HTTPStatusError as error:
        pd.DataFrame(imported).to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                + "error_during_upload.csv",
            ),
            index=False,
        )
        raise CastorException(
            str(error)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from error
    return instance


def upload_report(
    castorized_dataframe: pd.DataFrame,
    common: dict,
    upload_datetime: str,
    study: "CastorStudy",
    package_id: str,
) -> dict:
    """Uploads report data to the study."""
    feedback_total = {}
    imported = []

    for record_id, record_frame in tqdm(
        castorized_dataframe.groupby("record_id"), "Uploading Data"
    ):
        instances = create_report_instances(
            study, imported, package_id, record_id, record_frame
        )
        count = 0
        for row in record_frame.to_dict("records"):
            # Create body to send
            body = [
                {
                    "field_id": study.get_single_field(field).field_id,
                    "instance_id": instances[count],
                    "field_value": row[field],
                    "change_reason": f"api_upload_Report_{upload_datetime}",
                    "confirmed_changes": True,
                }
                for field in row
                # Exclude empty fields and record_id
                if (field != "record_id" and row[field] is not None)
            ]

            # Upload the data
            feedback_row = upload_report_data(
                body, study, imported, instances[count], row, common
            )
            count += 1
            try:
                feedback_total = update_feedback(
                    feedback_row, feedback_total, row, study
                )
            except CastorException as error:
                pd.DataFrame(imported).to_csv(
                    pathlib.Path(
                        pathlib.Path.cwd(),
                        "output",
                        f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                        + "error_during_upload.csv",
                    ),
                    index=False,
                )
                raise CastorException(
                    str(error)
                    + " caused at "
                    + str(row)
                    + ".\n See output folder for successful imports"
                ) from error

    # Save output
    pd.DataFrame(imported).to_csv(
        pathlib.Path(
            pathlib.Path.cwd(),
            "output",
            f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}" + "successful_upload.csv",
        ),
        index=False,
    )
    return feedback_total


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
        feedback_row = study.client.update_report_data_record(
            record_id=row["record_id"],
            report_id=instance,
            common=common,
            body=body,
        )
        imported.append(row)
    except HTTPStatusError as error:
        pd.DataFrame(imported).to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                + "error_during_upload.csv",
            ),
            index=False,
        )
        raise CastorException(
            str(error)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from error
    return feedback_row


def create_report_instances(
    study: "CastorStudy",
    imported: list,
    package_id: str,
    record: str,
    record_frame: pd.DataFrame,
) -> list:
    """Tries to create a new survey package instance of package and for record."""
    try:
        # Create a report for each row in the dataframe
        body = [
            {
                "report_id": package_id,
                "parent_id": None,
                "report_name_custom": f"{record} - api_upload_Report_"
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}-{row}",
            }
            for row in range(1, len(record_frame.index) + 1)
        ]

        instances = study.client.create_multiple_report_instances_record(
            record_id=record, body=body
        )

    except HTTPStatusError as error:
        pd.DataFrame(imported).to_csv(
            pathlib.Path(
                pathlib.Path.cwd(),
                "output",
                f"{datetime.now().strftime('%Y%m%d %H%M%S.%f')}"
                + "error_during_upload.csv",
            ),
            index=False,
        )
        raise CastorException(
            str(error)
            + " caused at "
            + str(record)
            + ".\n See output folder for successful imports"
        ) from error
    return [instance["id"] for instance in instances["success"]]
