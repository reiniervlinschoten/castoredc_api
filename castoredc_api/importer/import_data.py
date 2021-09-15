import pathlib
import pandas as pd

from datetime import datetime
from typing import TYPE_CHECKING, Dict, Optional

from httpx import HTTPStatusError
from tqdm import tqdm

from castoredc_api import CastorException
from castoredc_api.importer.helpers import create_upload, update_feedback

if TYPE_CHECKING:
    from castoredc_api import CastorStudy


def import_data(
    data_source_path: str,
    column_link_path: str,
    study: "CastorStudy",
    label_data: bool,
    target: str,
    target_name: Optional[str] = None,
    email: Optional[str] = None,
    translation_path: Optional[str] = None,
    merge_path: Optional[str] = None,
) -> Dict:
    """Takes a path to an xls(x) file, a path to an xls(x) file specifying the link between the external columns and
    the Castor columns and imports the data into Castor using the given study and target form name or Study. Study needs to be authenticated.
    Optionally one can define translation and merge files.
    """
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
    target_name: Optional[str],
    email: Optional[str],
) -> Dict:
    """Uploads each row from the castorized dataframe as a distinct form to the study linked to CastorClient."""
    # Shared Data
    upload_datetime = datetime.now().strftime("%Y%m%d %H%M%S")
    common = {
        "change_reason": f"api_upload_{target}_{upload_datetime}",
        "confirmed_changes": True,
    }

    if target == "Study":
        return upload_study(castorized_dataframe, common, upload_datetime, study)
    elif target == "Survey":
        target_form = next(
            (
                form
                for form in study.client.all_survey_packages()
                if form["name"] == target_name
            ),
            None,
        )
        return upload_survey(castorized_dataframe, study, target_form["id"], email)
    elif target == "Report":
        target_form = study.get_single_form_name(target_name)
        return upload_report(
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


def upload_study(
    castorized_dataframe: pd.DataFrame,
    common: Dict,
    upload_datetime: str,
    study: "CastorStudy",
) -> Dict:
    """Uploads study data to the study."""
    # Create the body for this report by using list comprehension and excluding the record_id and empty fields
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
            if (field != "record_id" and row[field] is not None)
        ]

        # Upload the data
        feedback_row = upload_study_data(body, study, common, imported, row)
        try:
            feedback_total = update_feedback(feedback_row, feedback_total, row, study)
        except CastorException as e:
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
                str(e)
                + " caused at "
                + str(row)
                + ".\n See output folder for successful imports"
            ) from e

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
    body: Dict, study: "CastorStudy", common: Dict, imported: list, row: "Dict"
):
    try:
        feedback_row = study.client.update_study_data_record(
            record_id=row["record_id"], common=common, body=body
        )
        imported.append(row)
    except HTTPStatusError as e:
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
            str(e)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from e
    return feedback_row


def upload_survey(
    castorized_dataframe: pd.DataFrame,
    study: "CastorStudy",
    package_id: str,
    email: str,
) -> Dict:
    """Uploads survey data to the study."""
    # Create the body for this report by using list comprehension and excluding the record_id and empty fields
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
            if (field != "record_id" and row[field] is not None)
        ]

        # Upload the data
        feedback_row = upload_survey_data(body, study, imported, instance, row)
        try:
            feedback_total = update_feedback(feedback_row, feedback_total, row, study)
        except CastorException as e:
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
                str(e)
                + " caused at "
                + str(row)
                + ".\n See output folder for successful imports"
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
    return feedback_total


def upload_survey_data(
    body: list, study: "CastorStudy", imported: list, instance: Dict, row: Dict
) -> Dict:
    """Tries to upload the survey data."""
    try:
        feedback_row = study.client.update_survey_package_instance_data_record(
            record_id=row["record_id"],
            survey_package_instance_id=instance["id"],
            body=body,
        )
        imported.append(row)
    except HTTPStatusError as e:
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
            str(e)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from e
    return feedback_row


def create_survey_package_instance(
    study: "CastorStudy", imported: list, package_id: str, row: Dict, email: str
) -> Dict:
    """Tries to create a new survey package instance of package and for record."""
    try:
        instance = study.client.create_survey_package_instance(
            survey_package_id=package_id,
            record_id=row["record_id"],
            email_address=email,
            auto_send=False,
        )
    except HTTPStatusError as e:
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
            str(e)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from e
    return instance


def upload_report(
    castorized_dataframe: pd.DataFrame,
    common: Dict,
    upload_datetime: str,
    study: "CastorStudy",
    package_id: str,
) -> Dict:
    """Uploads report data to the study."""
    # Create the body for this report by using list comprehension and excluding the record_id and empty fields
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
            except CastorException as e:
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
                    str(e)
                    + " caused at "
                    + str(row)
                    + ".\n See output folder for successful imports"
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
    return feedback_total


def upload_report_data(
    body: list,
    study: "CastorStudy",
    imported: list,
    instance: Dict,
    row: Dict,
    common: Dict,
) -> Dict:
    """Tries to upload the survey data."""
    try:
        feedback_row = study.client.update_report_data_record(
            record_id=row["record_id"],
            report_id=instance,
            common=common,
            body=body,
        )
        imported.append(row)
    except HTTPStatusError as e:
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
            str(e)
            + " caused at "
            + str(row)
            + ".\n See output folder for successful imports"
        ) from e
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
                "report_name_custom": f"{record} - api_upload_Report_{datetime.now().strftime('%Y%m%d %H%M%S.%f')}-{row}",
            }
            for row in range(1, len(record_frame.index) + 1)
        ]

        instances = study.client.create_multiple_report_instances_record(
            record_id=record, body=body
        )

    except HTTPStatusError as e:
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
            str(e)
            + " caused at "
            + str(record)
            + ".\n See output folder for successful imports"
        ) from e
    return [instance["id"] for instance in instances["success"]]
