# -*- coding: utf-8 -*-
"""
Testing class for audit trail endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/country

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError


class TestAuditTrail:
    def test_audit_trail_basic(self, write_client):
        """Test basic audit trail functionality"""
        audit_trail = write_client.audit_trail(
            date_from="2022-06-28", date_to="2022-06-28"
        )[0]
        assert audit_trail == self.test_audit_trail_model

    def test_audit_trail_fail(self, write_client):
        """Test audit trail fails correctly"""
        with pytest.raises(ValueError) as e:
            write_client.audit_trail(date_from="12-10-2021", date_to="12-10-2021")
        assert "does not match format" in str(e.value)

    def test_audit_trail_user(self, write_client):
        """Test audit trail functionality while filtering on user"""
        audit_trail = write_client.audit_trail(
            date_from="2022-06-28",
            date_to="2022-06-28",
            user_id="B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        )[0]
        assert audit_trail == self.test_audit_trail_model

    test_audit_trail_model = {
        "datetime": {
            "date": "2022-06-28 07:13:49.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "event_type": "Survey created",
        "user_id": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "user_role": None,
        "user_name": "Reinier van Linschoten",
        "user_email": "R.linschoten@franciscus.nl",
        "event_details": {
            "Allow Step Navigation": "0",
            "Auto Lock On Finish": "0",
            "Force Step Completion": "0",
            "Form Sync Id": "C75ADDCC-568B-4709-A46F-08723ED92072",
            "Show Step Navigator": "0",
            "Survey Auto Send": "0",
            "Survey Id": "8702EC31-0BB9-4BC2-A3A5-3101C4414246",
            "Survey Name": "Generalised Anxiety Disorder Questionnaire (GAD-7)",
            "Survey Reminder": "0",
            "Survey Required": "0",
            "Survey Send After": "0",
            "Survey Sender Address": "R.linschoten@franciscus.nl",
            "Survey Sender Name": "Reinier van Linschoten",
        },
    }
