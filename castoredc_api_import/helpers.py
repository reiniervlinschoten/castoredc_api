import numpy as np
import pandas as pd

from datetime import datetime
from typing import Dict, TYPE_CHECKING, Optional, List
from castoredc_api_client import CastorException


if TYPE_CHECKING:
    from castoredc_api_study import CastorStudy


def read_excel(path: str) -> pd.DataFrame:
    """Opens an xls(x) file as a pandas dataframe."""
    dataframe = pd.read_excel(path, dtype=str)
    dataframe = dataframe.where(pd.notnull(dataframe), None)
    # Remove columns without a header -> often Excel artefacts
    dataframe = dataframe[
        dataframe.columns.drop(list(dataframe.filter(regex="Unnamed:")))
    ]
    return dataframe


def create_column_translation(path: str) -> Dict:
    """Translates an excel sheet of column name links to a dict of column name translations"""
    link_dataframe = read_excel(path)
    translated_columns = {}
    # Transform dataframe to dict
    data_dict = link_dataframe.to_dict("index")
    # For every row in the dataframe, add the link to the dict
    for row in data_dict:
        other = data_dict[row]["other"]
        castor = data_dict[row]["castor"]
        # If there exists a link already, append it
        if other in translated_columns:
            translated_columns[other].append(castor)
        else:
            translated_columns[other] = [castor]
    return translated_columns


def castorize_column(
    to_import: pd.Series, new_name: list, label_data: bool, study: "CastorStudy"
) -> Dict:
    """Translates the values in a column to Castorized values ready for import."""
    # TODO: Add data validation with data validation from Castor database.
    if new_name[0] == "record_id":
        return {new_name[0]: to_import.tolist()}

    else:
        target_field = study.get_single_field(new_name[0])
        if target_field.field_type in ["checkbox", "dropdown", "radio"]:
            options = {
                option["name"]: option["value"]
                for option in study.get_single_optiongroup(
                    target_field.field_option_group
                )["options"]
            }
            if len(new_name) == 1:
                # There is no dependent 'other' field in the Castor database
                return castorize_optiongroup_column(
                    to_import, options, new_name[0], label_data
                )
            elif len(new_name) == 2:
                # Get the value for the parent that opens the dependent field
                parent_value = study.get_single_field(new_name[1]).field_dependency[
                    "parent_value"
                ]
                # Castorize the parent column
                parent_import = castorize_optiongroup_column(
                    to_import, options, new_name[0], label_data, parent_value
                )
                # Castorize the dependent column
                dep_import = castorize_dep_column(
                    to_import,
                    new_name[1],
                    pd.Series(parent_import[new_name[0]]),
                    parent_value,
                )
                return {**parent_import, **dep_import}
        elif target_field.field_type in ["numeric"]:
            return {new_name[0]: castorize_num_column(to_import.tolist())}
        elif target_field.field_type in ["year"]:
            return {new_name[0]: castorize_year_column(to_import.tolist())}
        elif target_field.field_type in ["slider"]:
            return {new_name[0]: castorize_num_column(to_import.tolist())}
        elif target_field.field_type in ["string", "textarea"]:
            return {new_name[0]: to_import.tolist()}
        elif target_field.field_type in ["date"]:
            return {new_name[0]: castorize_date_column(to_import.tolist())}
        elif target_field.field_type in ["datetime"]:
            return {new_name[0]: castorize_datetime_column(to_import.tolist())}
        elif target_field.field_type in ["time"]:
            return {new_name[0]: castorize_time_column(to_import.tolist())}
        elif target_field.field_type in ["numberdate"]:
            return {new_name[0]: castorize_numberdate_column(to_import.tolist())}
        else:
            raise CastorException(
                f"The field {target_field} is not importable with type {target_field.field_type}"
            )


def castorize_dep_column(
    to_import: pd.Series, new_name: str, parent_import: pd.Series, parent_value: str
):
    """Takes a column and extracts the values that need to be imported in the dependent column."""
    # Get the (checkbox can have multiple inputs) index where the 'other' field is used
    dep_position = parent_import.str.split(";").apply(get_index, args=(parent_value,))
    dep_position = dep_position.where(pd.notnull(dep_position), None)
    # Only keep the data where the 'other' field is checked
    vectorized_function = np.vectorize(get_value_at_index)
    dep_import = {
        new_name: vectorized_function(to_import.str.split(";"), dep_position).tolist()
    }
    return dep_import


def castorize_optiongroup_column(
    to_import: pd.Series,
    options: Dict,
    new_name: str,
    label_data: bool,
    parent_value: Optional[str] = None,
) -> Dict:
    """Takes a column with optiongroup data, splits it, translates it into castor data and merges it back"""
    to_import = to_import.str.split(";")
    to_import = to_import.apply(
        castorize_optiongroup_datapoint, args=(options, label_data, parent_value)
    )
    to_import = to_import.str.join(";")
    return {new_name: to_import.tolist()}


def castorize_optiongroup_datapoint(
    values: List, options: Dict, label_data: bool, parent_value: Optional[str]
) -> Optional[List]:
    """Translates a list of values split by ; into Castor Values."""
    # If the datapoint was empty, return an empty datapoint
    if values is None:
        new_values = None

    else:
        new_values = []
        # If labelled data was provided, translate this to optiongroup values (False or parent_value for failures)
        if label_data:
            for value in values:
                if parent_value is None:
                    new_values.append(options.get(str(value), "Error"))
                else:
                    new_values.append(options.get(str(value), parent_value))
        # If value data was provided, check if this exists in the optiongroup (False or parent_value for failures)
        else:
            for value in values:
                if parent_value is None:
                    if str(value) in options.values():
                        new_values.append(value)
                    else:
                        new_values.append("Error")
                else:
                    if str(value) in options.values():
                        new_values.append(value)
                    else:
                        new_values.append(parent_value)

    return new_values


def get_index(item: Optional[List], value: int):
    """Returns the index of the value in the list, else None."""
    if item is None:
        return None
    else:
        try:
            return item.index(value)
        except ValueError:
            return None


def get_value_at_index(item: Optional[List], index: Optional[float]):
    """Returns the index of the value in the list, else None."""
    if item is None or pd.isnull(index):
        return None
    else:
        return item[int(index)]


def castorize_num_column(data: List):
    """Castorizes a numeric column and replaces errors with 'Error'."""
    new_list = []
    for datapoint in data:
        if datapoint is None:
            new_list.append(None)
        else:
            try:
                # Test if data point is convertible to float
                float(datapoint)
                new_list.append(datapoint)
            except ValueError:
                new_list.append("Error")
    return new_list


def castorize_year_column(data: List):
    """Castorizes a year column and replaces errors with 'Error'."""
    new_list = []
    for datapoint in data:
        if datapoint is None:
            new_list.append(None)
        else:
            try:
                # Test if the data point is year-like. Sorry people from before 1900 and after 2100
                if 1900 < int(datapoint) < 2100:
                    new_list.append(datapoint)
                else:
                    new_list.append("Error")
            except ValueError:
                new_list.append("Error")
    return new_list


def castorize_date_column(data: List):
    """Castorizes a date column and replaces errors with 'Error'."""
    # TODO: add config file with preferred formats
    new_list = []
    for datapoint in data:
        if datapoint is None:
            new_list.append(None)
        else:
            try:
                # Try parsing the date
                parsed_date = datetime.strptime(datapoint, "%d-%m-%Y")
                new_list.append(parsed_date.strftime("%d-%m-%Y"))
            except ValueError:
                new_list.append("Error")
    return new_list


def castorize_datetime_column(data: List):
    """Castorizes a datetime column and replaces errors with 'Error'."""
    # TODO: add config file with preferred formats
    new_list = []
    for datapoint in data:
        if datapoint is None:
            new_list.append(None)
        else:
            try:
                # Try parsing the date
                parsed_date = datetime.strptime(datapoint, "%d-%m-%Y;%H:%M")
                new_list.append(parsed_date.strftime("%d-%m-%Y;%H:%M"))
            except ValueError:
                new_list.append("Error")
    return new_list


def castorize_time_column(data: List):
    """Castorizes a time column and replaces errors with 'Error'."""
    # TODO: add config file with preferred formats
    new_list = []
    for datapoint in data:
        if datapoint is None:
            new_list.append(None)
        else:
            try:
                # Try parsing the date
                parsed_date = datetime.strptime(datapoint, "%H:%M")
                new_list.append(parsed_date.strftime("%H:%M"))
            except ValueError:
                new_list.append("Error")
    return new_list


def castorize_numberdate_column(data: List):
    """Castorizes a numberdate column and replaces errors with 'Error'."""
    # TODO: add config file with preferred formats
    new_list = []
    for datapoint in data:
        if datapoint is None:
            new_list.append(None)

        else:
            split = datapoint.split(";")

            if len(split) != 2:
                new_list.append("Error")

            else:
                new_value = []

                # Try parsing the number
                try:
                    # Test if data point is convertible to float
                    float(split[0])
                    new_value.append(split[0])
                except ValueError:
                    new_value.append("Error")

                # Try parsing the date
                try:
                    parsed_date = datetime.strptime(split[1], "%d-%m-%Y")
                    new_value.append(parsed_date.strftime("%d-%m-%Y"))
                except ValueError:
                    new_value.append("Error")

                new_list.append(";".join(new_value))

    return new_list


def create_upload(
    path_to_upload: str, path_to_col_link: str, label_data: bool, study: "CastorStudy"
) -> pd.DataFrame:
    """Takes a path to an Excel file and returns a dataframe that is ready to be uploaded into Castor."""
    to_upload = read_excel(path_to_upload)
    column_translation = create_column_translation(path_to_col_link)
    new_data = {}
    for column in to_upload:
        new_column = castorize_column(
            to_import=to_upload[column],
            new_name=column_translation[column],
            label_data=label_data,
            study=study,
        )
        new_data = {**new_data, **new_column}
    return pd.DataFrame.from_dict(new_data)


def update_feedback(feedback_row, feedback_total, row, study):
    """Updates a dict of the form record_id: List of List of Dicts of CastorFields with the new information."""
    formatted_feedback_row = {
        "success": {
            study.get_single_field(field["field_id"]).field_name: field["field_value"]
            for field in feedback_row["success"]
        },
        "failed": {
            study.get_single_field(field["field_id"]).field_name: field["field_value"]
            for field in feedback_row["failed"]
        },
    }

    if row["record_id"] not in feedback_total:
        feedback_total[row["record_id"]] = [formatted_feedback_row]
    else:
        feedback_total[row["record_id"]].append(formatted_feedback_row)
    return feedback_total
