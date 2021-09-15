from typing import List
import pytest

import castoredc_api.study.castor_objects.castor_record as castor_record
import castoredc_api.study.castor_objects.castor_field as castor_field
import castoredc_api.study.castor_objects.castor_form as castor_form
import castoredc_api.study.castor_objects.castor_step as castor_step
import castoredc_api.study.castor_study as castor_study
from castoredc_api.study.castor_objects import (
    castor_data_point,
    castor_report_form_instance,
    castor_survey_form_instance,
    castor_study_form_instance,
    castor_form_instance,
)

from castoredc_api.tests.test_castor_objects.helpers_castor_objects import (
    link_study_with_forms,
    link_forms_with_steps,
    link_steps_with_fields,
    link_everything,
    link_study_with_records,
    link_instances_with_data_points,
    link_records_with_instances,
    link_data_to_structure,
)


@pytest.fixture(scope="function")
def fields() -> List[castor_field.CastorField]:
    """Creates CastorFields for use in tests."""
    field1 = castor_field.CastorField(
        field_id="FAKE-SURVEY-FIELD-ID1",
        field_name="Survey Field 1a1",
        field_label="This is the first survey field",
        field_type="test",
        field_required="0",
        field_option_group=None,
        field_order="1",
    )
    field2 = castor_field.CastorField(
        field_id="FAKE-SURVEY-FIELD-ID2",
        field_name="Survey Field 1a2",
        field_label="This is the second survey field",
        field_type="test",
        field_required="0",
        field_option_group=None,
        field_order="1",
    )
    field3 = castor_field.CastorField(
        field_id="FAKE-SURVEY-FIELD-ID3",
        field_name="Survey Field 1a3",
        field_label="This is the third survey field",
        field_type="test",
        field_required="0",
        field_option_group=None,
        field_order="1",
    )
    field4 = castor_field.CastorField(
        field_id="FAKE-SURVEY-FIELD-ID4",
        field_name="Survey Field 1b1",
        field_label="This is the first survey field",
        field_type="test",
        field_required="0",
        field_option_group=None,
        field_order="1",
    )
    field5 = castor_field.CastorField(
        field_id="FAKE-SURVEY-FIELD-ID5",
        field_name="Survey Field 1c1",
        field_label="This is the first survey field",
        field_type="test",
        field_required="0",
        field_option_group=None,
        field_order="1",
    )
    field6 = castor_field.CastorField(
        field_id="FAKE-SURVEY-FIELD-ID6",
        field_name="Survey Field 1c2",
        field_label="This is the second survey field",
        field_type="test",
        field_required="0",
        field_option_group=None,
        field_order="1",
    )
    field7 = castor_field.CastorField(
        field_id="FAKE-REPORT-FIELD-ID1",
        field_name="Report Field 1a1",
        field_label="This is the first report field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field8 = castor_field.CastorField(
        field_id="FAKE-REPORT-FIELD-ID2",
        field_name="Report Field 1a2",
        field_label="This is the second report field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field9 = castor_field.CastorField(
        field_id="FAKE-REPORT-FIELD-ID3",
        field_name="Report Field 1b1",
        field_label="This is the first report field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field10 = castor_field.CastorField(
        field_id="FAKE-REPORT-FIELD-ID4",
        field_name="Report Field 2a1",
        field_label="This is the first report field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field11 = castor_field.CastorField(
        field_id="FAKE-REPORT-FIELD-ID5",
        field_name="Report Field 2a2",
        field_label="This is the second report field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field12 = castor_field.CastorField(
        field_id="FAKE-REPORT-FIELD-ID6",
        field_name="Report Field 2a3",
        field_label="This is the third report field",
        field_type="date",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field13 = castor_field.CastorField(
        field_id="FAKE-REPORT-FIELD-ID7",
        field_name="Report Field 2a4",
        field_label="This is the fourth report field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field14 = castor_field.CastorField(
        field_id="FAKE-STUDY-FIELD-ID1",
        field_name="Study Field 1a1",
        field_label="This is the first study field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field15 = castor_field.CastorField(
        field_id="FAKE-STUDY-FIELD-ID2",
        field_name="Study Field 1b1",
        field_label="This is the first study field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field16 = castor_field.CastorField(
        field_id="FAKE-STUDY-FIELD-ID3",
        field_name="Study Field 1b2",
        field_label="This is the second study field",
        field_type="test",
        field_required="1",
        field_option_group=None,
        field_order="1",
    )
    field17 = castor_field.CastorField(
        field_id="FAKE-STUDY-FIELD-ID4",
        field_name="Study Field 1c1",
        field_label="This is the first study field",
        field_type="test",
        field_required="0",
        field_option_group=None,
        field_order="1",
    )
    return [
        field1,
        field2,
        field3,
        field4,
        field5,
        field6,
        field7,
        field8,
        field9,
        field10,
        field11,
        field12,
        field13,
        field14,
        field15,
        field16,
        field17,
    ]


@pytest.fixture(scope="function")
def steps() -> List[castor_step.CastorStep]:
    """Creates CastorSteps for use in tests."""
    step1 = castor_step.CastorStep("Survey Step 1a", "FAKE-SURVEY-STEP-ID1", "1")
    step2 = castor_step.CastorStep("Survey Step 1b", "FAKE-SURVEY-STEP-ID2", "1")
    step3 = castor_step.CastorStep("Survey Step 1c", "FAKE-SURVEY-STEP-ID3", "1")
    step4 = castor_step.CastorStep("Report Step 1a", "FAKE-REPORT-STEP-ID1", "1")
    step5 = castor_step.CastorStep("Report Step 1b", "FAKE-REPORT-STEP-ID2", "1")
    step6 = castor_step.CastorStep("Report Step 2a", "FAKE-REPORT-STEP-ID3", "1")
    step7 = castor_step.CastorStep("Study Step 1a", "FAKE-STUDY-STEP-ID1", "1")
    step8 = castor_step.CastorStep("Study Step 1b", "FAKE-STUDY-STEP-ID2", "1")
    step9 = castor_step.CastorStep("Study Step 1c", "FAKE-STUDY-STEP-ID3", "1")
    return [step1, step2, step3, step4, step5, step6, step7, step8, step9]


@pytest.fixture(scope="function")
def forms() -> List[castor_form.CastorForm]:
    """Creates CastorForms for use in tests."""
    form1 = castor_form.CastorForm("Fake Survey", "FAKE-SURVEY-ID1", "Survey", "1")
    form2 = castor_form.CastorForm("Fake Report 1", "FAKE-REPORT-ID1", "Report", "1")
    form3 = castor_form.CastorForm("Fake Report 2", "FAKE-REPORT-ID2", "Report", "1")
    form4 = castor_form.CastorForm(
        "Fake Study", "FAKE-STUDYIDFAKE-STUDYIDFAKE-STUDYID", "Study", "1"
    )
    return [form1, form2, form3, form4]


@pytest.fixture(scope="function")
def data_points(
    complete_study: castor_study.CastorStudy,
) -> List[castor_data_point.CastorDataPoint]:
    """Creates CastorDataPoints for use in tests."""
    data_point1 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID1", "2", complete_study, "2021-01-15 13:39:47"
    )
    data_point2 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID2", "test", complete_study, "2021-01-15 13:39:47"
    )
    data_point3 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID3", "1", complete_study, "2021-01-15 13:39:47"
    )

    data_point4 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID4", "test", complete_study, "2021-01-15 13:39:47"
    )
    data_point5 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID5", "2", complete_study, "2021-01-15 13:39:47"
    )

    data_point6 = castor_data_point.CastorDataPoint(
        "FAKE-REPORT-FIELD-ID1", "13", complete_study, "2021-01-15 13:39:47"
    )
    data_point7 = castor_data_point.CastorDataPoint(
        "FAKE-REPORT-FIELD-ID2", "-12", complete_study, "2021-01-15 13:39:47"
    )

    data_point8 = castor_data_point.CastorDataPoint(
        "FAKE-REPORT-FIELD-ID3", "0", complete_study, "2021-01-15 13:39:47"
    )

    data_point9 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID6", "2", complete_study, "2021-01-15 13:39:47"
    )

    data_point10 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID2", "test", complete_study, "2021-01-15 13:39:47"
    )

    data_point11 = castor_data_point.CastorDataPoint(
        "FAKE-STUDY-FIELD-ID1", "12", complete_study, "2021-01-15 13:39:47"
    )
    data_point12 = castor_data_point.CastorDataPoint(
        "FAKE-STUDY-FIELD-ID2",
        "01-12-2031;12:53",
        complete_study,
        "2021-01-15 13:39:47",
    )

    data_point13 = castor_data_point.CastorDataPoint(
        "FAKE-STUDY-FIELD-ID3", "2", complete_study, "2021-01-15 13:39:47"
    )
    data_point14 = castor_data_point.CastorDataPoint(
        "FAKE-STUDY-FIELD-ID4", "test", complete_study, "2021-01-15 13:39:47"
    )

    data_point15 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID3", "10", complete_study, "2021-01-15 13:39:47"
    )
    data_point16 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID2", "13", complete_study, "2021-01-15 13:39:47"
    )
    data_point17 = castor_data_point.CastorDataPoint(
        "FAKE-SURVEY-FIELD-ID1", "test", complete_study, "2021-01-15 13:39:47"
    )

    return [
        data_point1,
        data_point2,
        data_point3,
        data_point4,
        data_point5,
        data_point6,
        data_point7,
        data_point8,
        data_point9,
        data_point10,
        data_point11,
        data_point12,
        data_point13,
        data_point14,
        data_point15,
        data_point16,
        data_point17,
    ]


@pytest.fixture(scope="function")
def form_instances(
    complete_study: castor_study.CastorStudy,
) -> List[castor_form_instance.CastorFormInstance]:
    """Creates CastorFormInstances for use in tests."""
    form_instance1 = castor_survey_form_instance.CastorSurveyFormInstance(
        "FAKE-SURVEY-INSTANCE-ID1", "Fake Survey", complete_study
    )
    form_instance2 = castor_survey_form_instance.CastorSurveyFormInstance(
        "FAKE-SURVEY-INSTANCE-ID2", "Fake Survey", complete_study
    )
    form_instance3 = castor_report_form_instance.CastorReportFormInstance(
        "FAKE-REPORT-INSTANCE-ID1", "Report Name #91298", complete_study
    )
    form_instance4 = castor_report_form_instance.CastorReportFormInstance(
        "FAKE-REPORT-INSTANCE-ID2", "Report Name #90212", complete_study
    )

    form_instance5 = castor_survey_form_instance.CastorSurveyFormInstance(
        "FAKE-SURVEY-INSTANCE-ID3", "Fake Survey", complete_study
    )
    form_instance6 = castor_survey_form_instance.CastorSurveyFormInstance(
        "FAKE-SURVEY-INSTANCE-ID4", "Fake Survey", complete_study
    )

    # Data export does not return names of study form instance, but merely that field belongs to study
    form_instance7 = castor_study_form_instance.CastorStudyFormInstance(
        "FAKE-STUDYIDFAKE-STUDYIDFAKE-STUDYID", "Baseline", complete_study
    )
    form_instance8 = castor_study_form_instance.CastorStudyFormInstance(
        "FAKE-STUDYIDFAKE-STUDYIDFAKE-STUDYID", "Baseline", complete_study
    )

    form_instance9 = castor_survey_form_instance.CastorSurveyFormInstance(
        "FAKE-SURVEY-INSTANCE-ID5", "Fake Survey", complete_study
    )
    return [
        form_instance1,
        form_instance2,
        form_instance3,
        form_instance4,
        form_instance5,
        form_instance6,
        form_instance7,
        form_instance8,
        form_instance9,
    ]


@pytest.fixture(scope="function")
def records() -> List[castor_record.CastorRecord]:
    """Creates CastorRecords for use in tests."""
    record1 = castor_record.CastorRecord("110001")
    record2 = castor_record.CastorRecord("110002")
    record3 = castor_record.CastorRecord("110003")
    return [record1, record2, record3]


@pytest.fixture(scope="function")
def study() -> castor_study.CastorStudy:
    """Creates a CastorStudy for use in tests."""
    study = castor_study.CastorStudy("", "", "FAKE-ID", "", test=True)
    # Fake for tests
    study.form_links = {
        "Survey": {"Fake Survey": "FAKE-SURVEY-ID1"},
        "Report": {
            "FAKE-REPORT-INSTANCE-ID1": "FAKE-REPORT-ID1",
            "FAKE-REPORT-INSTANCE-ID2": "FAKE-REPORT-ID2",
        },
    }
    return study


@pytest.fixture(scope="function")
def study_with_forms(
    study: castor_study.CastorStudy, forms: List[castor_form.CastorForm]
) -> castor_study.CastorStudy:
    """Creates a CastorStudy with linked forms for use in tests."""
    return link_study_with_forms(study, forms)


@pytest.fixture(scope="function")
def forms_with_steps(
    forms: List[castor_form.CastorForm], steps: List[castor_step.CastorStep]
) -> List[castor_form.CastorForm]:
    """Creates CastorForms with linked steps for use in tests."""
    return link_forms_with_steps(forms, steps)


@pytest.fixture(scope="function")
def steps_with_fields(
    steps: List[castor_step.CastorStep], fields: List[castor_field.CastorField]
) -> List[castor_step.CastorStep]:
    """Creates CastorSteps with linked fields for use in tests."""
    return link_steps_with_fields(steps, fields)


@pytest.fixture(scope="function")
def complete_study(
    study: castor_study.CastorStudy,
    forms: List[castor_form.CastorForm],
    steps: List[castor_step.CastorStep],
    fields: List[castor_field.CastorField],
) -> castor_study.CastorStudy:
    """Creates a CastorStudy with linked forms, steps, and fields for use in tests."""
    return link_everything(study, forms, steps, fields)


@pytest.fixture(scope="function")
def study_with_records(
    complete_study: castor_study.CastorStudy, records: List[castor_record.CastorRecord]
) -> castor_study.CastorStudy:
    """Creates a CastorStudy with linked records for use in tests."""
    return link_study_with_records(complete_study, records)


@pytest.fixture(scope="function")
def records_with_form_instances(
    records: List[castor_record.CastorRecord],
    form_instances: List[castor_form_instance.CastorFormInstance],
) -> List[castor_record.CastorRecord]:
    """Creates CastorRecords with linked instances for use in tests."""
    return link_records_with_instances(records, form_instances)


@pytest.fixture(scope="function")
def instances_with_data_points(
    form_instances: List[castor_form_instance.CastorFormInstance],
    data_points: List[castor_data_point.CastorDataPoint],
) -> List[castor_form_instance.CastorFormInstance]:
    """Creates CastorForms with linked data points for use in tests."""
    return link_instances_with_data_points(form_instances, data_points)


@pytest.fixture(scope="function")
def complete_study_with_data(
    complete_study: castor_study.CastorStudy,
    records: List[castor_record.CastorRecord],
    form_instances: List[castor_form_instance.CastorFormInstance],
    data_points: List[castor_data_point.CastorDataPoint],
) -> castor_study.CastorStudy:
    """Creates a CastorStudy with linked forms, steps, and fields for use in tests."""
    return link_data_to_structure(complete_study, records, form_instances, data_points)
