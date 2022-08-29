# -*- coding: utf-8 -*-
"""
Testing class for survey endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/survey

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
from datetime import datetime

import pytest
import pytz
from httpx import HTTPStatusError

from castoredc_api import CastorException
from castoredc_api.tests.test_api_endpoints.data_models import (
    survey_model,
    package_model,
    survey_package_instance_model,
)


def create_survey_package_instance_body(record_id, fake):
    if fake:
        random_package = "FAKE"
    else:
        random_package = "4AAEDF4B-0137-46BD-BC4C-CC3E4BBF1588"

    return {
        "survey_package_id": random_package,
        "record_id": record_id,
        "ccr_patient_id": None,
        "email_address": "clearlyfakemail@itsascam.com",
        "package_invitation_subject": None,
        "package_invitation": None,
        "auto_send": None,
        "auto_lock_on_finish": None,
    }


class TestSurveyEndpoints:
    s_model_keys = survey_model.keys()
    p_model_keys = package_model.keys()
    i_model_keys = survey_package_instance_model.keys()

    test_survey = {
        "id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
        "survey_id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
        "name": "QOL Survey",
        "description": "",
        "intro_text": "##### This is the survey intro text. Here you can add some information for the participant that they will see before they start filling in the survey.\n```\n\n\n```\n##### Check the help text in the survey form editor to see how you can format this text or add images and links.\n```\n\n\n```\n### For example, you can use hashtags to make the text bigger or add headings.",
        "outro_text": "",
        "survey_steps": [],
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/survey/D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"
            }
        },
    }

    test_survey_package = {
        "id": "71C01598-4682-4A4C-90E6-69C0BD38EA47",
        "survey_package_id": "71C01598-4682-4A4C-90E6-69C0BD38EA47",
        "name": "My first survey package",
        "description": "",
        "sender_name": "Castor EDC",
        "auto_send": False,
        "allow_step_navigation": True,
        "show_step_navigator": True,
        "finish_url": "",
        "allow_open_survey_link": False,
        "auto_lock_on_finish": False,
        "intro_text": "```\n\n\n```\n#### To be able to send surveys, you have to create a survey package that will contain the survey(s) you want to send.\n```\n\n\n```\nHere you can add intro text. This is similar to the intro text in a survey itself, but since a survey package can contain multiple surveys, this is a 'general' introduction that appears in the very beginning.",
        "outro_text": "```\n\n\n```\n#### You can now create your own survey! \n```\n\n\n```\n#### Here is a giphy: \n```\n\n\n```\n![alt text](https://media.giphy.com/media/BUXk0VHa2Weis/giphy.gif).",
        "default_invitation": 'Dear participant,\n\nYou are participating in the study "Example Study" and we would like to ask you to fill in a survey.\n\nPlease click the link below to complete our survey.\n\n{url}\n\n{logo}',
        "default_invitation_subject": "Please fill in this survey for Example Study",
        "sender_email": "no-reply@castoredc.com",
        "is_mobile": False,
        "is_training": False,
        "is_repeatable": False,
        "is_resumable": False,
        "field_pagination": "none",
        "as_needed": False,
        "expire_after_hours": None,
        "_embedded": {
            "surveys": [
                {
                    "id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                    "survey_id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                    "name": "QOL Survey",
                    "description": "",
                    "intro_text": "##### This is the survey intro text. Here you can add some information for the participant that they will see before they start filling in the survey.\n```\n\n\n```\n##### Check the help text in the survey form editor to see how you can format this text or add images and links.\n```\n\n\n```\n### For example, you can use hashtags to make the text bigger or add headings.",
                    "outro_text": "",
                    "survey_steps": [],
                    "_links": {
                        "self": {
                            "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/survey/D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"
                        }
                    },
                }
            ]
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/surveypackage/71C01598-4682-4A4C-90E6-69C0BD38EA47"
            }
        },
    }

    test_survey_package_instance = {
        "id": "115DF660-A00A-4927-9E5F-A07D030D4A09",
        "survey_package_instance_id": "115DF660-A00A-4927-9E5F-A07D030D4A09",
        "record_id": "000001",
        "institute_id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
        "institute_name": "Test Institute",
        "survey_package_name": "My first survey package",
        "survey_package_id": "71C01598-4682-4A4C-90E6-69C0BD38EA47",
        "survey_url_string": "DUQKNQNN",
        "progress": 100,
        "received_on": None,
        "invitation_subject": "Please fill in this survey for Example Study",
        "invitation_content": 'Dear participant,\n\nYou are participating in the study "Example Study" and we would like to ask you to fill in a survey.\n\nPlease click the link below to complete our survey.\n\n{url}\n\n{logo}',
        "created_on": {
            "date": "2019-10-14 09:42:27.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "available_from": {
            "date": "2019-10-14 09:42:27.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "expire_on": None,
        "sent_on": None,
        "first_opened_on": None,
        "started_on": None,
        "all_fields_filled_on": None,
        "finished_on": {
            "date": "2020-08-14 16:27:12.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "locked": False,
        "archived": False,
        "auto_lock_on_finish": False,
        "auto_send": False,
        "_embedded": {
            "record": {
                "id": "000001",
                "record_id": "000001",
                "record_status": None,
                "ccr_patient_id": "",
                "last_opened_step": "1F1A5F3B-FD1A-45A6-9E0F-327F2EC68983",
                "progress": 28,
                "locked": False,
                "status": "open",
                "archived": False,
                "archived_reason": None,
                "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
                "created_on": {
                    "date": "2019-10-07 16:16:02.000000",
                    "timezone_type": 3,
                    "timezone": "Europe/Amsterdam",
                },
                "updated_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
                "updated_on": {
                    "date": "2021-10-20 14:25:16.000000",
                    "timezone_type": 3,
                    "timezone": "Europe/Amsterdam",
                },
                "randomized_id": None,
                "randomization_group": None,
                "randomization_group_name": None,
                "randomized_on": None,
                "_embedded": {
                    "institute": {
                        "id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                        "institute_id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                        "name": "Test Institute",
                        "abbreviation": "TES",
                        "date_format": "d-m-Y",
                        "code": "TES",
                        "order": 0,
                        "deleted": False,
                        "country_id": 169,
                        "_links": {
                            "self": {
                                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/institute/1CFF5802-0B07-471F-B97E-B5166332F2C5"
                            }
                        },
                    }
                },
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000001"
                    }
                },
            },
            "institute": {
                "id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                "institute_id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                "name": "Test Institute",
                "abbreviation": "TES",
                "date_format": "d-m-Y",
                "code": "TES",
                "order": 0,
                "deleted": False,
                "country_id": 169,
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/institute/1CFF5802-0B07-471F-B97E-B5166332F2C5"
                    }
                },
            },
            "survey_package": {
                "id": "71C01598-4682-4A4C-90E6-69C0BD38EA47",
                "survey_package_id": "71C01598-4682-4A4C-90E6-69C0BD38EA47",
                "name": "My first survey package",
                "description": "",
                "sender_name": "Castor EDC",
                "auto_send": False,
                "allow_step_navigation": True,
                "show_step_navigator": True,
                "finish_url": "",
                "auto_lock_on_finish": False,
                "intro_text": "```\n\n\n```\n#### To be able to send surveys, you have to create a survey package that will contain the survey(s) you want to send.\n```\n\n\n```\nHere you can add intro text. This is similar to the intro text in a survey itself, but since a survey package can contain multiple surveys, this is a 'general' introduction that appears in the very beginning.",
                "outro_text": "```\n\n\n```\n#### You can now create your own survey! \n```\n\n\n```\n#### Here is a giphy: \n```\n\n\n```\n![alt text](https://media.giphy.com/media/BUXk0VHa2Weis/giphy.gif).",
                "default_invitation": 'Dear participant,\n\nYou are participating in the study "Example Study" and we would like to ask you to fill in a survey.\n\nPlease click the link below to complete our survey.\n\n{url}\n\n{logo}',
                "default_invitation_subject": "Please fill in this survey for Example Study",
                "sender_email": "no-reply@castoredc.com",
                "is_mobile": False,
                "is_training": False,
                "is_repeatable": False,
                "is_resumable": False,
                "as_needed": False,
                "expire_after_hours": None,
                "field_pagination": "none",
                "allow_open_survey_link": False,
                "_embedded": {
                    "surveys": [
                        {
                            "id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                            "survey_id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                            "name": "QOL Survey",
                            "description": "",
                            "intro_text": "##### This is the survey intro text. Here you can add some information for the participant that they will see before they start filling in the survey.\n```\n\n\n```\n##### Check the help text in the survey form editor to see how you can format this text or add images and links.\n```\n\n\n```\n### For example, you can use hashtags to make the text bigger or add headings.",
                            "outro_text": "",
                            "survey_steps": [],
                            "_links": {
                                "self": {
                                    "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/survey/D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"
                                }
                            },
                        }
                    ]
                },
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/surveypackage/71C01598-4682-4A4C-90E6-69C0BD38EA47"
                    }
                },
            },
            "survey_instances": [
                {
                    "id": "6530D4AB-4705-4864-92AE-B0EC6200E8E5",
                    "progress": 100,
                    "progress_total_fields": 5,
                    "progress_total_fields_not_empty": 5,
                    "_embedded": {
                        "survey": {
                            "id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                            "survey_id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                            "name": "QOL Survey",
                            "description": "",
                            "intro_text": "##### This is the survey intro text. Here you can add some information for the participant that they will see before they start filling in the survey.\n```\n\n\n```\n##### Check the help text in the survey form editor to see how you can format this text or add images and links.\n```\n\n\n```\n### For example, you can use hashtags to make the text bigger or add headings.",
                            "outro_text": "",
                            "survey_steps": [],
                            "_links": {
                                "self": {
                                    "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/survey/D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"
                                }
                            },
                        }
                    },
                    "_links": {
                        "self": {
                            "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/survey/6530D4AB-4705-4864-92AE-B0EC6200E8E5"
                        }
                    },
                }
            ],
            "survey_reminders": [],
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/surveypackageinstance/115DF660-A00A-4927-9E5F-A07D030D4A09"
            }
        },
    }

    @pytest.fixture
    def all_surveys(self, client):
        """Get all surveys"""
        all_surveys = client.all_surveys()
        return all_surveys

    @pytest.fixture
    def all_survey_packages(self, client):
        """Get all survey packages"""
        all_survey_packages = client.all_survey_packages()
        return all_survey_packages

    @pytest.fixture
    def all_survey_package_instances(self, client):
        """Get all survey package instances"""
        all_survey_package_instances = client.all_survey_package_instances()
        return all_survey_package_instances

    # SURVEYS
    def test_all_surveys(self, all_surveys):
        """Test the structure returned by all_surveys"""
        for survey in all_surveys:
            survey_keys = survey.keys()
            assert len(survey_keys) == len(self.s_model_keys)
            for key in survey_keys:
                assert key in self.s_model_keys
                assert type(survey[key]) in survey_model[key]

    def test_single_survey_success(self, client, all_surveys):
        """Test the structure and data returned by single survey"""
        survey = client.single_survey("D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E")
        assert survey == self.test_survey

    def test_single_survey_fail(self, client, all_surveys):
        """Test calling on a non-existent survey"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey("D70C1273-B5D8-45CD-BFE8-A0BA75C4FAKE")
        assert e.value.response.status_code == 404

    # SURVEY PACKAGES
    def test_all_survey_packages(self, all_survey_packages):
        """Test structure returned by all_survey_packages"""
        for package in all_survey_packages:
            package_keys = package.keys()
            assert len(package_keys) == len(self.p_model_keys)
            for key in package_keys:
                assert key in self.p_model_keys
                assert type(package[key]) in package_model[key]

    def test_single_survey_package_success(self, client, all_survey_packages):
        """Test structure and data returned by single_survey_package"""
        package = client.single_survey_package("71C01598-4682-4A4C-90E6-69C0BD38EA47")
        assert package == self.test_survey_package

    def test_single_survey_package_fail(self, client, all_survey_packages):
        """Test calling on a non-existent survey package"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_package("71C01598-4682-4A4C-90E6-69C0BD38FAKE")
        assert e.value.response.status_code == 404

    # SURVEY PACKAGE INSTANCES
    def test_all_survey_package_instances(self, all_survey_package_instances):
        """Test structure returned by all survey package instances"""
        for package_instance in all_survey_package_instances:
            instance_keys = package_instance.keys()
            assert len(instance_keys) == len(self.i_model_keys)
            for key in instance_keys:
                assert key in self.i_model_keys
                assert type(package_instance[key]) in survey_package_instance_model[key]

    def test_all_survey_package_instance_record_success(
        self, client, all_survey_package_instances
    ):
        """Test structure retuned by all_survey_package_instances after filtering on record"""
        instances = client.all_survey_package_instances(record_id="000002")

        for instance in instances:
            assert instance["record_id"] == "000002"
            instance_keys = instance.keys()
            assert len(instance_keys) == len(self.i_model_keys)
            for key in instance_keys:
                assert key in self.i_model_keys
                assert type(instance[key]) in survey_package_instance_model[key]

    def test_survey_package_instance_filtered_success(
        self, client, all_survey_package_instances
    ):
        """Test data returned by all_survey_package_instances after filtering on finish date"""
        instances = client.all_survey_package_instances(
            record_id="000001", finished_on="2020-08-14"
        )
        assert len(instances) == 1
        assert instances[0] == self.test_survey_package_instance

    def test_survey_package_instance_filtered_fail_double_record_id(
        self, client, all_survey_package_instances
    ):
        """Test all_survey_package_instances filtering errors correctly"""
        with pytest.raises(CastorException) as e:
            client.all_survey_package_instances(
                record_id="000001", ccr_patient_id="000001"
            )
        assert "Cannot supply both record_id and ccr_patient_id" in str(e.value)

    def test_survey_package_instance_filtered_fail_wrong_date_format(
        self, client, all_survey_package_instances
    ):
        """Test all_survey_package_instances filtering errors correctly"""
        with pytest.raises(HTTPStatusError) as e:
            client.all_survey_package_instances(
                record_id="000001", finished_on="14-08-2020"
            )
        assert e.value.response.status_code == 422

    def test_all_survey_package_instance_record_fail(
        self, client, all_survey_package_instances
    ):
        """Test filtering on non-existent record"""
        with pytest.raises(HTTPStatusError) as e:
            client.all_survey_package_instances(record_id="00FAKE")
        assert e.value.response.status_code == 404

    def test_single_survey_package_instance_success(
        self, client, all_survey_package_instances
    ):
        """Test data and structure returned by selecting single survey."""
        instance = client.single_survey_package_instance(
            "115DF660-A00A-4927-9E5F-A07D030D4A09"
        )
        assert instance == self.test_survey_package_instance

    def test_single_survey_package_instance_fail(
        self, client, all_survey_package_instances
    ):
        """Test querying a non-existent survey."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_package_instance(
                "115DF660-A00A-4927-9E5F-A07D030DFAKE"
            )
        assert e.value.response.status_code == 404

    # POST
    def test_create_survey_package_instance_success(self, write_client):
        """Tests creating a new survey package instance"""
        old_amount = len(write_client.all_survey_package_instances(record_id="110001"))
        body = create_survey_package_instance_body("110001", fake=False)

        feedback = write_client.create_survey_package_instance(**body)

        new_amount = len(write_client.all_survey_package_instances(record_id="110001"))

        assert feedback["record_id"] == "110001"
        assert new_amount == old_amount + 1

    def test_create_survey_package_instance_fail(self, write_client):
        """Tests failing to create a new survey package instance by wrong survey_instance_id"""
        body = create_survey_package_instance_body("110001", fake=True)
        old_amount = len(write_client.all_survey_package_instances(record_id="110001"))

        with pytest.raises(HTTPStatusError) as e:
            write_client.create_survey_package_instance(**body)
        assert e.value.response.status_code == 422

        new_amount = len(write_client.all_survey_package_instances(record_id="110001"))
        assert new_amount == old_amount

    def test_lock_unlock_survey_package_instance_success(self, write_client):
        """Tests patching (locking/unlocking) a survey_package_instance"""
        package = write_client.single_survey_package_instance(
            "CEF2F230-9F52-45C7-A92D-27B93A5E2B23"
        )
        old_status = package["locked"]

        target_status = not old_status
        write_client.lock_unlock_survey_package_instance(
            "CEF2F230-9F52-45C7-A92D-27B93A5E2B23", target_status
        )

        package = write_client.single_survey_package_instance(
            "CEF2F230-9F52-45C7-A92D-27B93A5E2B23"
        )
        new_status = package["locked"]
        assert new_status is not old_status

    def test_lock_unlock_survey_package_instance_failure(self, write_client):
        """Tests failing to lock/unlock a survey_package_instance"""
        package = write_client.single_survey_package_instance(
            "CEF2F230-9F52-45C7-A92D-27B93A5E2B23"
        )
        old_status = package["locked"]
        target_status = not old_status
        fake_id = "23B4FD48-BA41-4C9B-BAEF-D5C3DD5FFAKE"

        with pytest.raises(HTTPStatusError) as e:
            write_client.lock_unlock_survey_package_instance(fake_id, target_status)
        assert e.value.response.status_code == 404

        package = write_client.single_survey_package_instance(
            "CEF2F230-9F52-45C7-A92D-27B93A5E2B23"
        )
        new_status = package["locked"]
        assert new_status is old_status

    def test_patch_survey_package_instance_start_time_success(self, client):
        """Tests patching the start time of a survey_package_instance"""
        package = client.single_survey_package_instance(
            "3936CDF8-7F8E-45B4-9957-1BCEEAC78DD4"
        )
        old_started_on = package["started_on"]["date"]
        now = datetime.now(pytz.utc)
        now_string = now.strftime("%Y-%m-%d %H:%M:%S")

        client.update_start_time_survey_package_instance(
            "000001", "3936CDF8-7F8E-45B4-9957-1BCEEAC78DD4", now_string
        )

        package = client.single_survey_package_instance(
            "3936CDF8-7F8E-45B4-9957-1BCEEAC78DD4"
        )
        new_started_on = package["started_on"]["date"]
        assert new_started_on != old_started_on
        # Need to give UTC timezone to Castor, but returns Time zone in local datetime
        assert (
            now.astimezone(pytz.timezone("Europe/Amsterdam")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            in new_started_on
        )

    def test_patch_survey_package_instance_start_time_failure(self, client):
        """Tests failing to patch the start time of a survey_package_instance"""
        package = client.single_survey_package_instance(
            "3936CDF8-7F8E-45B4-9957-1BCEEAC78DD4"
        )
        old_started_on = package["started_on"]["date"]
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        fake_id = "3936CDF8-7F8E-45B4-9957-1BCEEAC7FAKE"

        with pytest.raises(HTTPStatusError) as e:
            client.update_start_time_survey_package_instance("000001", fake_id, now)
        assert e.value.response.status_code == 404

        package = client.single_survey_package_instance(
            "3936CDF8-7F8E-45B4-9957-1BCEEAC78DD4"
        )
        new_started_on = package["started_on"]["date"]
        assert new_started_on == old_started_on
