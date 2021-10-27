"""Module to import data to Castor EDC using the API"""
import asyncio
from datetime import datetime
import typing
import pathlib
from castoredc_api import CastorException
from castoredc_api.importer.async_import import upload_data_async
from castoredc_api.importer.helpers import create_upload
from castoredc_api.importer.sync_import import upload_data

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
    if use_async:
        upload = upload_data_async(
            castorized_dataframe, study, target, target_name, email
        )
    else:
        upload = upload_data(castorized_dataframe, study, target, target_name, email)
    return upload
