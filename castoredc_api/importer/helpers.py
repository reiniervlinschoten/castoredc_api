import numpy as np
import pandas as pd

from datetime import datetime
from typing import Dict, TYPE_CHECKING, Optional, List
from castoredc_api import CastorException

if TYPE_CHECKING:
    from castoredc_api.study import CastorStudy


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


def create_variable_translation(path: str) -> Dict:
    """Translates an excel sheet of variable values or labels to a dict of variable translations"""
    translation_dataframe = read_excel(path)
    translated_values = {}
    # Transform dataframe to dict
    data_dict = translation_dataframe.to_dict("index")
    # For every row in the dataframe, add the link to the dict
    for row in data_dict:
        variable = data_dict[row]["variable"]
        other = data_dict[row]["other"]
        castor = data_dict[row]["castor"]
        # If there exists a link already, append it
        if variable in translated_values:
            translated_values[variable][other] = castor
        else:
            translated_values[variable] = {other: castor}
    return translated_values


def create_merge_translation(path: str) -> Dict:
    """Translates an excel sheet of merge links to a dict of merge links"""
    link_dataframe = read_excel(path)
    merge_column_dict = {"variable_translations": {}, "column_links": {}}
    # Transform dataframe to dict
    data_dict = link_dataframe.to_dict("index")
    # For every row in the dataframe, add the link to the dict
    for row in data_dict:
        # Exctract data
        other_variable = data_dict[row]["other_variable"]
        other_value = data_dict[row]["other_value"]
        castor_variable = data_dict[row]["castor_variable"]
        castor_value = data_dict[row]["castor_value"]
        # Link columns if they are not already linked
        if castor_variable in merge_column_dict["column_links"]:
            if other_variable not in merge_column_dict["column_links"][castor_variable]:
                merge_column_dict["column_links"][castor_variable].append(
                    other_variable
                )
        else:
            merge_column_dict["column_links"][castor_variable] = [other_variable]
        if other_variable in merge_column_dict["variable_translations"]:
            merge_column_dict["variable_translations"][other_variable][
                other_value
            ] = castor_value
        else:
            merge_column_dict["variable_translations"][other_variable] = {
                other_value: castor_value
            }
    return merge_column_dict


def castorize_column(
    to_import: pd.Series,
    new_name: list,
    label_data: bool,
    study: "CastorStudy",
    variable_translation: Dict,
) -> Dict:
    """Translates the values in a column to Castorized values ready for import."""
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
                    to_import,
                    options,
                    new_name[0],
                    label_data,
                    None,
                    variable_translation,
                )
            elif len(new_name) == 2:
                # Get the value for the parent that opens the dependent field
                parent_value = study.get_single_field(new_name[1]).field_dependency[
                    "parent_value"
                ]
                # Castorize the parent column
                parent_import = castorize_optiongroup_column(
                    to_import,
                    options,
                    new_name[0],
                    label_data,
                    parent_value,
                    variable_translation,
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
    parent_value: Optional[str],
    variable_translation: Optional[Dict],
) -> Dict:
    """Takes a column with optiongroup data, splits it, translates it into castor data and merges it back"""
    other_name = to_import.name
    # Split the string into a list based on the ; seperator
    to_import = to_import.str.split(";")
    # To each list or None element in the series, translate the value/label to the correct optiongroup value
    to_import = to_import.apply(
        castorize_optiongroup_datapoint,
        args=(options, label_data, parent_value, variable_translation, other_name),
    )
    # Merge them to a ; seperated string for import in castor
    to_import = to_import.str.join(";")
    return {new_name: to_import.tolist()}


def castorize_optiongroup_datapoint(
    values: List,
    options: Dict,
    label_data: bool,
    parent_value: Optional[str],
    variable_translation: Optional[Dict],
    other_name: str,
) -> Optional[List]:
    """Translates a list of values split by ; into Castor Values."""
    # If the datapoint was None or NaN, return an empty datapoint
    if not isinstance(values, list):
        if pd.isnull(values):
            new_values = None

    else:
        new_values = []
        translate_dict = get_translation_dict(other_name, variable_translation)
        # If labelled data was provided, translate this to optiongroup values (False or parent_value for failures)
        if label_data:
            new_values = translate_value_data(
                new_values, options, parent_value, translate_dict, values
            )
        # If value data was provided, check if this exists in the optiongroup (False or parent_value for failures)
        else:
            new_values = translate_label_data(
                new_values, options, parent_value, translate_dict, values
            )
    return new_values


def translate_label_data(
    new_values: list,
    options: dict,
    parent_value: str,
    translate_dict: Optional[Dict],
    values: list,
):
    """Translates label data if necessary and checks if it falls within the Castor optiongroup"""
    translate = False if translate_dict is None else True
    for value in values:
        if pd.isnull(parent_value):
            if translate:
                value = translate_dict.get(str(value), "Error")
            if str(value) in options.values():
                new_values.append(value)
            else:
                new_values.append("Error")
        else:
            if translate:
                value = translate_dict.get(str(value), parent_value)
            if str(value) in options.values():
                new_values.append(value)
            else:
                new_values.append(parent_value)
    return new_values


def translate_value_data(
    new_values: list,
    options: dict,
    parent_value: str,
    translate_dict: Optional[Dict],
    values: list,
):
    """Translates value data if necessary and checks if it falls within the Castor optiongroup"""
    translate = False if translate_dict is None else True
    for value in values:
        if pd.isnull(parent_value):
            if translate:
                value = translate_dict.get(str(value), "Error")
            new_values.append(options.get(str(value), "Error"))
        else:
            if translate:
                value = translate_dict.get(str(value), parent_value)
            new_values.append(options.get(str(value), parent_value))
    return new_values


def get_translation_dict(other_name: str, variable_translation: Dict) -> Optional[Dict]:
    """Returns the translation dict or None if no translation necessary."""
    # Translate if variable_translation exists
    if variable_translation is None:
        translate_dict = None
    else:
        try:
            # Sometimes not all variables are translated, only set translate to true if this variable has a
            # translation dict
            translate_dict = variable_translation[other_name]
        except KeyError:
            translate_dict = None
    return translate_dict


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


def translate_merge(value: Optional[str], translation: dict) -> str:
    """Translates a value to the new column value."""
    if pd.isnull(value):
        return np.nan
    else:
        return translation.get(str(value), "Error")


def merge_row(row: pd.Series) -> str:
    """Merges multiple columns in a row to a single column."""
    row = row.dropna()
    row = ";".join(row.values.astype(str))
    row = np.nan if row == "" else row
    return row


def merge_columns(to_upload: pd.DataFrame, path_to_merge: str) -> pd.DataFrame:
    """Merges multiple columns as defined in path_to_merge to a single column"""
    merge_link = create_merge_translation(path_to_merge)
    # Translate Values
    for other_variable in merge_link["variable_translations"]:
        to_upload[other_variable] = to_upload[other_variable].apply(
            translate_merge, args=(merge_link["variable_translations"][other_variable],)
        )
    # Merge Columns
    for castor_variable in merge_link["column_links"]:
        to_upload[castor_variable] = to_upload[
            merge_link["column_links"][castor_variable]
        ].apply(merge_row, axis=1)
        to_upload = to_upload.drop(columns=merge_link["column_links"][castor_variable])

    return to_upload


def create_upload(
    path_to_upload: str,
    path_to_col_link: str,
    path_to_translation: Optional[str],
    path_to_merge: Optional[str],
    label_data: bool,
    study: "CastorStudy",
) -> pd.DataFrame:
    """Takes a path to an Excel file and returns a dataframe that is ready to be uploaded into Castor."""
    to_upload = read_excel(path_to_upload)
    # Merge columns into a single one
    if path_to_merge is not None:
        to_upload = merge_columns(to_upload, path_to_merge)
    # Create translation dicts
    column_translation = create_column_translation(path_to_col_link)
    variable_translation = (
        create_variable_translation(path_to_translation)
        if path_to_translation is not None
        else None
    )
    new_data = {}
    for column in to_upload:
        new_column = castorize_column(
            to_import=to_upload[column],
            new_name=column_translation[column],
            label_data=label_data,
            study=study,
            variable_translation=variable_translation,
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
            study.get_single_field(field["field_id"]).field_name: [
                field["code"],
                field["message"],
            ]
            for field in feedback_row["failed"]
        },
    }

    if row["record_id"] not in feedback_total:
        feedback_total[row["record_id"]] = [formatted_feedback_row]
    else:
        feedback_total[row["record_id"]].append(formatted_feedback_row)

    if len(formatted_feedback_row["failed"]) > 0:
        raise CastorException(formatted_feedback_row["failed"])

    return feedback_total
