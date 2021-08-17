from typing import List

import castoredc_api.study.castor_objects.castor_field as castor_field
import castoredc_api.study.castor_objects.castor_form as castor_form
import castoredc_api.study.castor_objects.castor_step as castor_step
import castoredc_api.study.castor_study as castor_study
from castoredc_api.study.castor_objects import (
    castor_data_point,
    castor_form_instance,
    castor_record,
)


def link_study_with_forms(
    study: castor_study.CastorStudy, forms: List[castor_form.CastorForm]
) -> castor_study.CastorStudy:
    """Takes a list of forms and links them to a study."""
    for form in forms:
        study.add_form(form)
    return study


def link_forms_with_steps(
    forms: List[castor_form.CastorForm], steps: List[castor_step.CastorStep]
) -> List[castor_form.CastorForm]:
    """Takes a list of steps and links them to a list of forms."""
    for step in steps[:3]:
        forms[0].add_step(step)

    for step in steps[3:5]:
        forms[1].add_step(step)

    forms[2].add_step(steps[5])

    for step in steps[6:]:
        forms[3].add_step(step)

    return forms


def link_steps_with_fields(
    steps: List[castor_step.CastorStep], fields: List[castor_field.CastorField]
) -> List[castor_step.CastorStep]:
    """Takes a list of fields and links them to a list of steps."""
    for field in fields[0:3]:
        steps[0].add_field(field)

    steps[1].add_field(fields[3])

    for field in fields[4:6]:
        steps[2].add_field(field)

    for field in fields[6:8]:
        steps[3].add_field(field)

    steps[4].add_field(fields[8])

    for field in fields[9:13]:
        steps[5].add_field(field)

    steps[6].add_field(fields[13])

    for field in fields[14:16]:
        steps[7].add_field(field)

    steps[8].add_field(fields[16])

    return steps


def link_everything(
    study: castor_study.CastorStudy,
    forms: List[castor_form.CastorForm],
    steps: List[castor_step.CastorStep],
    fields: List[castor_field.CastorField],
) -> castor_study.CastorStudy:
    """Links a list of fields to a list of steps to a list of forms to a study."""
    steps = link_steps_with_fields(steps, fields)
    forms = link_forms_with_steps(forms, steps)
    study = link_study_with_forms(study, forms)
    return study


def link_data_to_structure(
    study: castor_study.CastorStudy,
    records: List[castor_record.CastorRecord],
    form_instances: List[castor_form_instance.CastorFormInstance],
    data_points: List[castor_data_point.CastorDataPoint],
) -> castor_study.CastorStudy:
    """Links a list of fields to a list of steps to a list of forms to a study."""
    form_instances = link_instances_with_data_points(form_instances, data_points)
    records = link_records_with_instances(records, form_instances)
    study = link_study_with_records(study, records)
    return study


def link_study_with_records(
    study: castor_study.CastorStudy, records: List[castor_record.CastorRecord]
) -> castor_study.CastorStudy:
    """Takes a list of records and links them to a study."""
    for record in records:
        study.add_record(record)
    return study


def link_records_with_instances(
    records: List[castor_record.CastorRecord],
    instances: List[castor_form_instance.CastorFormInstance],
) -> List[castor_record.CastorRecord]:
    """Takes a list of instances and links them to a list of records."""
    for instance in instances[:4]:
        records[0].add_form_instance(instance)

    for instance in instances[4:7]:
        records[1].add_form_instance(instance)

    for instance in instances[8:]:
        records[2].add_form_instance(instance)

    return records


def link_instances_with_data_points(
    instances: List[castor_form_instance.CastorFormInstance],
    data_points: List[castor_data_point.CastorDataPoint],
) -> List[castor_form_instance.CastorFormInstance]:
    """Takes a list of data_points and links them to a list of instances."""
    for data_point in data_points[0:3]:
        instances[0].add_data_point(data_point)

    for data_point in data_points[3:5]:
        instances[1].add_data_point(data_point)

    for data_point in data_points[5:7]:
        instances[2].add_data_point(data_point)

    instances[3].add_data_point(data_points[7])

    instances[4].add_data_point(data_points[8])

    instances[5].add_data_point(data_points[9])

    for data_point in data_points[10:12]:
        instances[6].add_data_point(data_point)

    for data_point in data_points[12:14]:
        instances[7].add_data_point(data_point)

    for data_point in data_points[14:17]:
        instances[8].add_data_point(data_point)

    return instances
