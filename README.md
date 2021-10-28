# CastorEDC API
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![pylint](https://github.com/reiniervlinschoten/castoredc_api/actions/workflows/pylint.yml/badge.svg)](https://github.com/reiniervlinschoten/castoredc_api/actions/workflows/pylint.yml)
[![pytest](https://github.com/reiniervlinschoten/castoredc_api/actions/workflows/pytest.yml/badge.svg)](https://github.com/reiniervlinschoten/castoredc_api/actions/workflows/pytest.yml)
[![coverage](https://img.shields.io/codecov/c/github/reiniervlinschoten/castoredc_api)](https://app.codecov.io/gh/reiniervlinschoten/castoredc_api)
[![black](https://github.com/reiniervlinschoten/castoredc_api/actions/workflows/black.yml/badge.svg)](https://github.com/reiniervlinschoten/castoredc_api/actions/workflows/black.yml)

[![pypi](https://img.shields.io/pypi/v/castoredc_api)](https://pypi.org/project/castoredc-api/)
[![conda](https://img.shields.io/conda/v/reiniervl/castoredc_api)](https://anaconda.org/reiniervl/castoredc_api)
[![conda-forge](https://img.shields.io/conda/v/conda-forge/castoredc_api)](https://anaconda.org/conda-forge/castoredc_api)

## Features
This is a Python package for interacting with the API of Castor Electronic Data Capture (EDC). 
The package contains functions to interact with all the endpoints defined on https://data.castoredc.com/api#/.
Within the package are functions for easy export and import of your data through the API.

### Export
Supported export formats are
* Pandas
* CSV
* R (using Feather)

### Import
Import currently only supports .xlsx files with some configuration.  
See for more information below.

## Getting Started
1. Install the package 
   * `pip install castoredc-api`
   * `conda install -c conda-forge castoredc_api`
   * `conda install -c reiniervl castoredc_api`
2. Import the client
3. Instantiate the client with your client-ID and client-secret (don't share these!) and url to the server.
   * ID and secret: Account -> Settings -> Castor EDC API
   * url: *region*.castoredc.com
4. Link the client to your study with the study-ID
   * ID: Study -> Settings -> Castor Study ID
5. Use the wrapper functions to start working with your study.

For all implemented functions, see: https://data.castoredc.com/api#/

```python
from castoredc_api import CastorClient

# Create a client with your credentials
c = CastorClient('MYCLIENTID', 
                 'MYCLIENTSECRET', 
                 'data.castoredc.com')

# Link the client to your study in the Castor EDC database
c.link_study('MYSTUDYID')

# Then you can interact with the API
# Get all records
c.all_records()

# Create a new survey package
c.create_survey_package_instance(survey_package_id="FAKESURVEY-PACKAGE-ID",
                                 record_id="TEST-RECORD",
                                 email_address="obviously@fakeemail.com",
                                 auto_send=True)
```

### Export
1. Instantiate the CastorStudy with your credentials, study ID and server url.
2. Use the Study functions to start working with your database

For exporting data: The endpoint that extracts data for the study can't be used if the authenticated user has a role within the study.  
See: https://data.castoredc.com/api#/export/get_study__study_id__export_data


```python
from castoredc_api import CastorStudy

# Instantiate Study
study = CastorStudy('MYCLIENTID', 
                    'MYCLIENTSECRET', 
                    'MYSTUDYID', 
                    'data.castoredc.com')

# Export your study to pandas dataframes or CSV files
study.export_to_dataframe()
study.export_to_csv()

# Data and structure mapping are automatically done on export, but you can also map these without exporting your data
# Map your study data locally (also maps structure)
study.map_data()

# Map only your study structure locally
study.map_structure()

# After mapping data and/or structure, you can start working with your study
# Get all reports
study.get_all_report_forms()
# Get all data points of a single record
study.get_single_record('000011').get_all_data_points()
```

#### Data Formatting
Date fields are returned as strings (dd-mm-yyyy)  
Datetime fields are returned as strings (dd-mm-yyyy hh-mm)  
Numeric fields are all returned as floats.

This can be changed by supplying the argument format_options when intialising the CastorStudy.  
Allowed options are date, datetime, datetime_seconds and time.  
See https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior for formatting options.

```python
from castoredc_api import CastorStudy

# Instantiate Study with different formatting settings
study = CastorStudy('MYCLIENTID', 
                    'MYCLIENTSECRET', 
                    'MYSTUDYID', 
                    'data.castoredc.com', 
                    format_options={
                      "date": "%B %e %Y",
                      "datetime": "%B %e %Y %I:%M %p",
                      "datetime_seconds": "%B %e %Y %I:%M:%S %p",
                      "time": "%I:%M %p",
                    })
```

#### Missing Data
Missing data is mostly handled through pandas (NaN).

User-defined missing data is handled through its definitions in Castor.  
For numeric and text-like variables, these values are -95, -96, -97, -98 and -99.  
For datetime data, missing data values are with the years 2995, 2996, 2997, 2998, and 2999.  

### Import
1. Instantiate the CastorStudy with your credentials, study ID and server url.
2. Format your data in the right format (see below)
3. Create a link file to link external and Castor variables (see below)
4. (Optional) Create a variable translation file to translate values and labels to Castor optiongroups (see below).
5. (Optional) Create a merge file to merge multiple columns into one CastorField (see below).
6. (Optional) Set date, datetime and time formatting to translate local format into Castor format (see below).
7. Import your data with the import_data function.
   * If label_data is set to true, it translates the string values to their integer values of the optiongroup in Castor.
   * If set to false, it takes the integer values as is.

Data is validated against the Castor database, meaning that:
* Existence of records and fields is checked
* Numeric values are compared against allowed values (min & max)
* Date(time) and time formats are compared against the specified format

#### Synchronous Upload
The synchronous upload option uploads each row one by one.  
When an Error is encountered or the upload finishes successfully, the program outputs the upload log to the output folder and stops.
 
#### Asynchronous Upload
The asynchronous upload option uploads each row one by one.  
This is about 15-30 times faster than synchronous upload.  
The program does not stop if uploading a row encounters an error.  
When the upload finishes, the program outputs the upload log to the output folder and stops.  
Error messages are stored in the output folder for debugging.

#### Simple Example

```python
from castoredc_api import CastorStudy
from castoredc_api import import_data

# Create a Study with your credentials
study = CastorStudy('MYCLIENTID',
                    'MYCLIENTSECRET',
                    'MYSTUDYID',
                    'data.castoredc.com')

# Import labelled study data
imported_data = import_data(data_source_path="PATH/TO/YOUR/LABELLED/STUDY/DATA",
                            column_link_path="PATH/TO/YOUR/LINK/FILE", 
                            study=study, 
                            label_data=True, 
                            target="Study")

# Import labelled study data (asynchronous)
imported_data = import_data(data_source_path="PATH/TO/YOUR/LABELLED/STUDY/DATA",
                            column_link_path="PATH/TO/YOUR/LINK/FILE", 
                            study=study, 
                            label_data=True, 
                            target="Study",
                            use_async=True)

# Import non-labelled report data
imported_data = import_data(data_source_path="PATH/TO/YOUR/REPORT/DATA", 
                            column_link_path="PATH/TO/YOUR/LINK/FILE",
                            study=study, 
                            label_data=False, 
                            target="Report", 
                            target_name="Medication")

# Import labelled survey data
imported_data = import_data(data_source_path="PATH/TO/YOUR/LABELLED/SURVEY/DATA",
                            column_link_path="PATH/TO/YOUR/LINK/FILE", 
                            study=study, 
                            label_data=True, 
                            target="Survey",
                            target_name="My first survey package", 
                            email="python_wrapper@you-spam.com")
```
#### Specifying the data structure
#### Data files
See below and example_files/ for an examples.
* Dates should be formatted as dd-mm-yyyy.
* Datetime should be formatted as dd-mm-yyyy;hh:mm
* Use semicolons for fields that allow multiple options (e.g. checkboxes)
* If any value for a column is translated, all values should have a translation mapped (see below)

##### Labels
The mg/4 weeks and mg/8 weeks under units will be imported to the med_other_unit fields as they do not match any option of the optiongroup, see link files.

##### Example

| patient | medication   | startdate  | stopdate   | dose | units      |
| ------- | ------------ | ---------- | ---------- | ---- | ---------- |
| 110001  | Azathioprine | 05-12-2019 | 05-12-2020 | 0.05 | g/day      |
| 110002  | Vedolizumab  | 17-08-2018 | 17-09-2020 | 300  | mg/4 weeks |
| 110003  | Ustekinumab  | 19-12-2017 | 03-06-2019 | 90   | mg/8 weeks |
| 110004  | Thioguanine  | 25-04-2020 | 27-05-2021 | 15   | mg/day     |
| 110005  | Tofacitinib  | 01-03-2020 | 31-12-2999 | 10   | mg/day     |

##### Values
The non-integer variables under units will be imported to the med_other_unit fields as they do not match any optionvalue of the optiongroup, see link files.

##### Example

| patient | medication   | startdate  | stopdate   | dose | units      |
| ------- | ------------ | ---------- | ---------- | ---- | ---------- |
| 110001  | Azathioprine | 05-12-2019 | 05-12-2020 | 0.05 | 3          |
| 110002  | Vedolizumab  | 17-08-2018 | 17-09-2020 | 300  | mg/4 weeks |
| 110003  | Ustekinumab  | 19-12-2017 | 03-06-2019 | 90   | mg/8 weeks |
| 110004  | Thioguanine  | 25-04-2020 | 27-05-2021 | 15   | 2          |
| 110005  | Tofacitinib  | 01-03-2020 | 31-12-2999 | 10   | 2          |


##### Link files
Link files should be of the format as shown below.
The mapping is variable name in the Excel file -> variable name in Castor.
If a variable in other is referenced twice in the Castor column, it means that it has a dependency in Castor.

This is a way to import data that has an "other" category, for example a radio question that reads:
* A
* B
* C
* Other

In which case selecting other opens a new text box to enter this information. 
The second variable in the link_file should be this new text box.

This is treated in the following manner:
* First, the data is mapped to the first variable referenced
* For all data that could not be mapped to the first variable, the 'other' category is selected in the first variable
* Then the data that could not be mapped is written to the second variable referenced.

##### Example

| other      | castor           |
| ---------- | ---------------- |
| patient    | record\_id       |
| medication | med\_name        |
| startdate  | med\_start       |
| stopdate   | med\_stop        |
| dose       | med\_dose        |
| units      | med\_units       |
| units      | med\_other\_unit |

##### Translation files
Translation files link the optiongroup value or label from the external database to the optiongroups from Castor.
Values are translated for all variables specified in the first column of the file.

Two situations can occur when a value is encountered for which no translation is given:
* If a dependent field is specified (see link files): the value is not translated and imported to the dependent field.
* If no dependent field is specified: the program gives an error. In this situation, every value that occurs in the external database needs to be mapped.

##### Example
| variable               | other                  | castor                              |
| ---------------------- | ---------------------- | ----------------------------------- |
| family disease history | none                   | None                                |
| family disease history | don't know             | Unknown                             |
| family disease history | deaf                   | Deafness                            |
| family disease history | cardiomyopathy         | (Cardio)myopathy                    |
| family disease history | encephalopathy         | Encephalopathy                      |
| family disease history | diabetes               | Diabetes Mellitus                   |
| family disease history | cardiovascular disease | Hypertension/Cardiovascular disease |
| family disease history | thromboembolism        | Thrombosis                          |
| family disease history | tumor                  | Malignancy                          |

```python
from castoredc_api import CastorStudy
from castoredc_api import import_data

# Create a Study with your credentials
study = CastorStudy('MYCLIENTID',
                    'MYCLIENTSECRET',
                    'MYSTUDYID',
                    'data.castoredc.com')

# Import study data with a translation file
imported_data = import_data(data_source_path="PATH/TO/YOUR/LABELLED/STUDY/DATA",
                            column_link_path="PATH/TO/YOUR/LINK/FILE", 
                            study=study, 
                            label_data=True, 
                            target="Study",
                            translation_path="PATH/TO/YOUR/TRANSLATION/FILE")
```

##### Merge files
Merge files link the multiple columns from the external database to a single checkbox field in Castor.  
For each column from the external database specified under other_variable the value under other_value is mapped to the castor_value for the castor_variable.  
If specifying a merge file, note that castor_value is the new other variable for your link file (see below).  
All other_values not defined raise an Error.
Only supports many-to-one matching.

##### Example

###### Data File
| patient | date baseline blood sample | baseline hemoglobin | factor V Leiden | datetime onset stroke | time onset trombectomy | year of birth | patient sex | patient race    | famhist\_none | famhist\_deaf | famhist\_cardiomyopathy | famhist\_encephalopathy | famhist\_diabmell | famhist\_cardiovasc | famhist\_malignancy | famhist\_unknown |
| ------- | -------------------------- | ------------------- | --------------- | --------------------- | ---------------------- | ------------- | ----------- | --------------- | ------------- | ------------- | ----------------------- | ----------------------- | ----------------- | ------------------- | ------------------- | ---------------- |
| 110001  | 16-03-2021                 | 8.3                 | 55;16-03-2021   | 16-03-2021;07:30      | 09:25                  | 1999          | Female      | Asian           | No            | No            | Yes                     | Yes                     | Yes               | No                  | No                  | No               |
| 110002  | 17-03-2021                 | 7.2                 | 33;17-03-2021   | 17-03-2021;15:30      | 06:33                  | 1956          | Female      | African/black   | No            | Yes           | Yes                     | No                      | No                | No                  | No                  | No               |
| 110003  | 16-03-2022                 | 9.1                 | \-45;18-03-2022 | 18-03-2022;02:00      | 12:24                  | 1945          | Male        | Chinese         | Yes           | No            | No                      | No                      | No                | No                  | No                  | No               |
| 110004  | 17-03-2022                 | 3.2                 | 28;19-03-2022   | 17-03-2022;21:43      | 23:23                  | 1933          | Male        | Caucasian/white | No            | No            | No                      | No                      | No                | Yes                 | Yes                 | No               |
| 110005  | 16-03-2023                 | 10.3                | 5;20-03-2023    | 16-03-2023;07:22      | 08:14                  | 1921          | Female      | Hispanic        | No            | No            | No                      | No                      | No                | No                  | No                  | Yes              |

###### Merge File

| other\_variable         | other\_value | castor\_variable | castor\_value                       |
| ----------------------- | ------------ | ---------------- | ----------------------------------- |
| famhist\_none           | Yes          | his\_family      | None                                |
| famhist\_deaf           | Yes          | his\_family      | Deafness                            |
| famhist\_cardiomyopathy | Yes          | his\_family      | (Cardio)myopathy                    |
| famhist\_encephalopathy | Yes          | his\_family      | Encephalopathy                      |
| famhist\_diabmell       | Yes          | his\_family      | Diabetes Mellitus                   |
| famhist\_cardiovasc     | Yes          | his\_family      | Hypertension/Cardiovascular disease |
| famhist\_malignancy     | Yes          | his\_family      | Malignancy                          |
| famhist\_unknown        | Yes          | his\_family      | Unknown                             |
| famhist\_none           | No           | his\_family      |                                     |
| famhist\_deaf           | No           | his\_family      |                                     |
| famhist\_cardiomyopathy | No           | his\_family      |                                     |
| famhist\_encephalopathy | No           | his\_family      |                                     |
| famhist\_diabmell       | No           | his\_family      |                                     |
| famhist\_cardiovasc     | No           | his\_family      |                                     |
| famhist\_malignancy     | No           | his\_family      |                                     |
| famhist\_unknown        | No           | his\_family      |                                     |

###### Link File

| other                      | castor             |
| -------------------------- | ------------------ |
| patient                    | record\_id         |
| date baseline blood sample | base\_bl\_date     |
| baseline hemoglobin        | base\_hb           |
| factor V Leiden            | fac\_V\_leiden     |
| datetime onset stroke      | onset\_stroke      |
| time onset trombectomy     | onset\_trombectomy |
| year of birth              | pat\_birth\_year   |
| patient sex                | pat\_sex           |
| patient race               | pat\_race          |
| **his\_family**            | **his\_family**    |

```python
from castoredc_api import CastorStudy
from castoredc_api import import_data

# Create a Study with your credentials
study = CastorStudy('MYCLIENTID',
                    'MYCLIENTSECRET',
                    'MYSTUDYID',
                    'data.castoredc.com')

# Import study data with a merge file
imported_data = import_data(data_source_path="PATH/TO/YOUR/LABELLED/STUDY/DATA",
                            column_link_path="PATH/TO/YOUR/LINK/FILE", 
                            study=study, 
                            label_data=True, 
                            target="Study",
                            merge_path="PATH/TO/YOUR/MERGE/FILE")
```

#### Data Formatting
Standard date formatting settings are the following.
Date(time) and time fields should follow these formats in the Excel sheet to be uploaded.
- Date = dd-mm-yyyy  
- Datetime = dd-mm-yyyy;hh-mm
- Time = hh:mm  
- Decimal separator = . 

These can be changed by supplying the argument format_options when calling create upload.  
Allowed options are date, datetime, and time. Decimal separator cannot be changed.  
See https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior for formatting options.

```python
from castoredc_api import CastorStudy
from castoredc_api import import_data

# Create a Study with your credentials
study = CastorStudy('MYCLIENTID',
                    'MYCLIENTSECRET',
                    'MYSTUDYID',
                    'data.castoredc.com')

# Import labelled study data with changed formats
imported_data = import_data(data_source_path="PATH/TO/YOUR/LABELLED/STUDY/DATA",
                            column_link_path="PATH/TO/YOUR/LINK/FILE", 
                            study=study, 
                            label_data=True, 
                            target="Study",
                            format_options={
                               "date": "%B %d %Y",
                               "datetime": "%B %d %Y %I:%M %p",
                               "time": "%I:%M %p",
                            })
```
## Prerequisites

1. Python Version >= 3.8
2. See [requirements.txt](requirements.txt)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/reiniervlinschoten/castoredc_api/tags). 

## Authors

* **R.C.A. van Linschoten** - *Initial Development* - [Reinier van Linschoten](https://github.com/reiniervlinschoten)

See also the list of [contributors](https://github.com/reiniervlinschoten/castoredc_api/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Franciscus Gasthuis & Vlietland for making time available for development  
* Castor EDC for support and code review
