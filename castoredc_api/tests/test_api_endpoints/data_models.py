# -*- coding: [stf-8 -*-
"""
Contains the definition of all data models according to the Castor EDC API.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

country_model = {
    "id": [
        str,
    ],
    "country_id": [
        str,
    ],
    "country_name": [
        str,
    ],
    "country_tld": [
        str,
    ],
    "country_cca2": [
        str,
    ],
    "country_cca3": [
        str,
    ],
}

single_country_model = {
    "id": [
        int,
    ],
    "country_id": [
        int,
    ],
    "country_name": [
        str,
    ],
    "country_tld": [
        str,
    ],
    "country_cca2": [
        str,
    ],
    "country_cca3": [
        str,
    ],
    "_links": [
        dict,
    ],
}

export_data_model = {
    "Study ID": [
        str,
    ],
    "Record ID": [
        str,
    ],
    "Form Type": [
        str,
    ],
    "Form Instance ID": [
        str,
    ],
    "Form Instance Name": [
        str,
    ],
    "Field ID": [
        str,
    ],
    "Value": [
        str,
    ],
    "Date": [
        str,
    ],
    "User ID": [
        str,
    ],
}

export_structure_model = {
    "Study ID": [
        str,
    ],
    "Form Type": [
        str,
    ],
    "Form Collection ID": [
        str,
    ],
    "Form Collection Name": [
        str,
    ],
    "Form Collection Order": [
        str,
    ],  # Actually int in database, but csv interprets everything as string
    "Form ID": [
        str,
    ],
    "Form Name": [
        str,
    ],
    "Form Order": [
        str,
    ],  # Actually int in database, but csv interprets everything as string
    "Field ID": [
        str,
    ],
    "Field Variable Name": [
        str,
    ],
    "Field Label": [
        str,
    ],
    "Field Type": [
        str,
    ],
    "Field Order": [
        str,
    ],  # Actually int in database, but csv interprets everything as string
    "Field Required": [
        str,
    ],  # Actually bool in database, but csv interprets everything as string
    "Calculation Template": [
        str,
    ],
    "Field Option Group": [
        str,
    ],
}

export_option_group_model = {
    "Study ID": [
        str,
    ],
    "Option Group Id": [
        str,
    ],
    "Option Group Name": [
        str,
    ],
    "Option Id": [
        str,
    ],
    "Option Name": [
        str,
    ],
    "Option Value": [
        str,
    ],
}

study_data_point_model = {
    "field_id": [
        str,
    ],
    "field_value": [
        str,
    ],
    "record_id": [
        str,
    ],
    "updated_on": [str, type(None)],
}

study_data_point_extended_model = {
    "record_id": [
        str,
    ],
    "field_variable_name": [
        str,
    ],
    "field_id": [
        str,
    ],
    "value": [
        str,
    ],
    "updated_on": [str, type(None)],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

study_step_model = {
    "id": [
        str,
    ],
    "step_id": [
        str,
    ],
    "step_description": [
        str,
    ],
    "step_name": [
        str,
    ],
    "step_order": [
        int,
    ],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

user_model = {
    "id": [
        str,
    ],
    "user_id": [
        str,
    ],
    "entity_id": [
        str,
    ],
    "full_name": [
        str,
    ],
    "name_first": [str, type(None)],
    "name_middle": [str, type(None)],
    "name_last": [str, type(None)],
    "email_address": [
        str,
    ],
    "institute": [str, type(None)],
    "department": [str, type(None)],
    "last_login": [
        str,
    ],
    "_links": [
        dict,
    ],
}

study_model = {
    "crf_id": [
        str,
    ],
    "study_id": [
        str,
    ],
    "name": [
        str,
    ],
    "created_by": [
        str,
    ],
    "created_on": [
        str,
    ],
    "live": [
        bool,
    ],
    "randomization_enabled": [
        bool,
    ],
    "gcp_enabled": [
        bool,
    ],
    "surveys_enabled": [
        bool,
    ],
    "premium_support_enabled": [
        bool,
    ],
    "main_contact": [
        str,
    ],
    "expected_centers": [int, type(None)],
    "duration": [int, type(None)],
    "expected_records": [int, type(None)],
    "slug": [
        str,
    ],
    "version": [
        str,
    ],
    "domain": [
        str,
    ],
    "_links": [
        dict,
    ],
}

report_model = {
    "id": [
        str,
    ],
    "report_id": [
        str,
    ],
    "description": [
        str,
    ],
    "name": [
        str,
    ],
    "type": [
        str,
    ],
    "_links": [
        dict,
    ],
}

report_instance_model = {
    "id": [
        str,
    ],
    "name": [
        str,
    ],
    "status": [
        str,
    ],
    "parent_id": [
        str,
    ],
    "parent_type": [
        str,
    ],
    "record_id": [
        str,
    ],
    "report_name": [
        str,
    ],
    "archived": [
        bool,
    ],
    "created_on": [
        str,
    ],
    "created_by": [
        str,
    ],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

report_data_point_model = {
    "field_id": [
        str,
    ],
    "report_instance_id": [
        str,
    ],
    "report_instance_name": [
        str,
    ],
    "field_value": [
        str,
    ],
    "record_id": [
        str,
    ],
    "updated_on": [
        str,
    ],
}

report_data_point_extended_model = {
    "record_id": [
        str,
    ],
    "field_variable_name": [
        str,
    ],
    "field_id": [
        str,
    ],
    "value": [
        str,
    ],
    "updated_on": [
        str,
    ],
    "report_instance_id": [
        str,
    ],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

report_step_model = {
    "id": [
        str,
    ],
    "report_step_id": [
        str,
    ],
    "report_step_name": [
        str,
    ],
    "report_step_description": [
        str,
    ],
    "report_step_number": [
        int,
    ],
    "_links": [
        dict,
    ],
    "_embedded": [
        dict,
    ],
}

survey_model = {
    "id": [
        str,
    ],
    "survey_id": [
        str,
    ],
    "name": [
        str,
    ],
    "description": [
        str,
    ],
    "intro_text": [
        str,
    ],
    "outro_text": [
        str,
    ],
    "survey_steps": [
        list,
    ],
    "_links": [
        dict,
    ],
}

package_model = {
    "id": [
        str,
    ],
    "survey_package_id": [
        str,
    ],
    "name": [
        str,
    ],
    "description": [
        str,
    ],
    "intro_text": [
        str,
    ],
    "outro_text": [
        str,
    ],
    "sender_name": [
        str,
    ],
    "sender_email": [
        str,
    ],
    "auto_send": [
        bool,
    ],
    "allow_step_navigation": [
        bool,
    ],
    "show_step_navigator": [
        bool,
    ],
    "finish_url": [
        str,
    ],
    "auto_lock_on_finish": [
        bool,
    ],
    "default_invitation": [
        str,
    ],
    "default_invitation_subject": [
        str,
    ],
    "is_mobile": [bool],
    "expire_after_hours": [int, type(None)],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

survey_package_instance_model = {
    "id": [
        str,
    ],
    "survey_package_instance_id": [
        str,
    ],
    "record_id": [
        str,
    ],
    "institute_id": [
        str,
    ],
    "institute_name": [
        str,
    ],
    "survey_package_id": [
        str,
    ],
    "survey_package_name": [
        str,
    ],
    "invitation_subject": [
        str,
    ],
    "invitation_content": [
        str,
    ],
    "created_on": [
        dict,
    ],
    "created_by": [
        str,
    ],
    "sent_on": [dict, type(None)],
    "first_opened_on": [dict, type(None)],
    "finished_on": [dict, type(None)],
    "available_from": [dict],
    "expire_on": [str, type(None)],
    "locked": [
        bool,
    ],
    "archived": [
        bool,
    ],
    "survey_url_string": [
        str,
    ],
    "progress": [
        int,
    ],
    "auto_lock_on_finish": [
        bool,
    ],
    "auto_send": [
        bool,
    ],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

survey_data_point_model = {
    "field_id": [
        str,
    ],
    "survey_instance_id": [
        str,
    ],
    "survey_name": [
        str,
    ],
    "field_value": [
        str,
    ],
    "record_id": [
        str,
    ],
    "updated_on": [
        str,
    ],
}

survey_package_data_point_model = {
    "field_id": [
        str,
    ],
    "survey_instance_id": [
        str,
    ],
    "survey_name": [
        str,
    ],
    "field_value": [
        str,
    ],
    "record_id": [
        str,
    ],
    "updated_on": [
        str,
    ],
    "survey_package_id": [
        str,
    ],
}

survey_data_point_extended_model = {
    "record_id": [
        str,
    ],
    "field_variable_name": [
        str,
    ],
    "field_id": [
        str,
    ],
    "value": [
        str,
    ],
    "updated_on": [
        str,
    ],
    "survey_instance_id": [
        str,
    ],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

survey_step_model = {
    "id": [
        str,
    ],
    "survey_step_id": [
        str,
    ],
    "survey_step_name": [
        str,
    ],
    "survey_step_description": [
        str,
    ],
    "survey_step_number": [
        int,
    ],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

field_dep_model = {
    "id": [
        str,
    ],
    "operator": [
        str,
    ],
    "value": [
        str,
    ],
    "parent_id": [
        str,
    ],
    "child_id": [
        str,
    ],
    "_links": [
        dict,
    ],
}

field_model = {
    "id": [
        str,
    ],
    "parent_id": [
        str,
    ],
    "field_id": [
        str,
    ],
    "field_number": [
        int,
    ],
    "field_label": [
        str,
    ],
    "field_variable_name": [str, type(None)],
    "field_type": [
        str,
    ],
    "field_required": [
        int,
    ],
    "field_hidden": [
        int,
    ],
    "field_info": [
        str,
    ],
    "field_units": [
        str,
    ],
    "field_min": [
        int,
        float,
        type(None),
    ],
    "field_min_label": [
        str,
        type(None),
    ],
    "field_max": [
        int,
        float,
        type(None),
    ],
    "field_max_label": [
        str,
        type(None),
    ],
    "field_summary_template": [
        str,
        type(None),
    ],
    "field_slider_step": [
        str,
        int,
        type(None),
    ],
    "report_id": [
        str,
    ],
    "field_length": [
        int,
        type(None),
    ],
    "additional_config": [
        str,
    ],
    "exclude_on_data_export": [
        bool,
    ],
    "option_group": [
        dict,
        type(None),
    ],
    "metadata_points": [
        list,
    ],
    "validations": [
        list,
    ],
    "dependency_parents": [
        list,
    ],
    "dependency_children": [
        list,
    ],
    "_links": [
        dict,
    ],
}

field_opt_model = {
    "id": [
        str,
    ],
    "name": [
        str,
    ],
    "description": [
        str,
    ],
    "layout": [
        bool,
    ],
    "options": [
        list,
    ],
    "_links": [
        dict,
    ],
}

field_val_model = {
    "id": [
        int,
    ],
    "type": [
        str,
    ],
    "value": [
        str,
    ],
    "operator": [
        str,
    ],
    "text": [
        str,
    ],
    "field_id": [
        str,
    ],
    "_links": [
        dict,
    ],
}

institute_model = {
    "id": [
        str,
    ],
    "institute_id": [
        str,
    ],
    "name": [
        str,
    ],
    "abbreviation": [
        str,
    ],
    "code": [str, type(None)],
    "order": [
        int,
    ],
    "country_id": [
        int,
    ],
    "deleted": [
        bool,
    ],
    "_links": [
        dict,
    ],
}

metadata_model = {
    "id": [
        str,
    ],
    "metadata_type": [
        dict,
    ],
    "parent_id": [str, type(None)],
    "value": [
        str,
    ],
    "description": [str, type(None)],
    "element_type": [
        str,
    ],
    "element_id": [str],
    "_links": [
        dict,
    ],
}

metadata_type_model = {
    "id": [
        int,
    ],
    "name": [
        str,
    ],
    "description": [
        str,
    ],
    "_links": [
        dict,
    ],
}

phase_model = {
    "id": [
        str,
    ],
    "phase_id": [
        str,
    ],
    "phase_description": [str, type(None)],
    "phase_name": [
        str,
    ],
    "phase_duration": [int, type(None)],
    "phase_order": [
        int,
    ],
    "_links": [
        dict,
    ],
}

query_model = {
    "id": [
        str,
    ],
    "record_id": [
        str,
    ],
    "field_id": [
        str,
    ],
    "status": [
        str,
    ],
    "first_query_remark": [
        str,
    ],
    "created_by": [
        str,
    ],
    "created_on": [
        dict,
    ],
    "updated_by": [
        str,
    ],
    "updated_on": [
        dict,
    ],
    "_embedded": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

record_model = {
    "id": [
        str,
    ],
    "record_id": [
        str,
    ],
    "_embedded": [
        dict,
    ],
    "ccr_patient_id": [
        str,
    ],
    "randomized_id": [str, type(None)],
    "randomization_group": [str, type(None)],
    "randomization_group_name": [str, type(None)],
    "randomized_on": [dict, type(None)],
    "last_opened_step": [str, type(None)],
    "progress": [
        int,
    ],
    "status": [
        str,
    ],
    "archived": [
        bool,
    ],
    "archived_reason": [str, type(None)],
    "created_by": [
        str,
    ],
    "created_on": [
        dict,
    ],
    "updated_by": [
        str,
    ],
    "updated_on": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

record_progress_model = {
    "record_id": [
        str,
    ],
    "steps": [
        list,
    ],
    "_links": [
        dict,
    ],
}

steps_model = {
    "step_id": [
        str,
    ],
    "complete": [
        int,
    ],
    "sdv": [
        bool,
    ],
    "locked": [
        bool,
    ],
    "signed": [
        bool,
    ],
}

statistics_model = {
    "study_id": [
        str,
    ],
    "records": [
        dict,
    ],
    "_links": [
        dict,
    ],
}

stats_records_model = {
    "total_count": [
        int,
    ],
    "institutes": [
        list,
    ],
}

stats_institutes_model = {
    "institute_id": [
        str,
    ],
    "institute_name": [
        str,
    ],
    "record_count": [
        int,
    ],
}
data_options = {
    "numeric": "1",
    "date": "11-11-2017",
    "string": "testing",
    "dropdown": "1",
    "radio": "1",
    "textarea": "testing",
    "slider": "5",
    "checkbox": "1",
    "calculation": "5",
    "year": "2005",
}
