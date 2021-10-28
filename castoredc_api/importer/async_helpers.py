import asyncio
import copy
import sys
import typing

import httpx
from httpx import HTTPStatusError
from tqdm import tqdm

from castoredc_api.importer.helpers import create_survey_body, create_report_body

if typing.TYPE_CHECKING:
    from castoredc_api import CastorStudy


async def async_update_study_data(data: list, study: "CastorStudy") -> list:
    """Updates the Castor EDC database with given study datapoints."""
    # Split list to handle error when len(tasks) > max_connections
    chunks = [
        data[x : x + study.client.max_connections]
        for x in range(0, len(data), study.client.max_connections)
    ]
    responses = []
    for idx, chunk in enumerate(chunks):
        async with httpx.AsyncClient(
            headers=study.client.headers,
            timeout=study.client.timeout,
            limits=study.client.limits,
        ) as client:
            tasks = [async_upload_study_data(item, client, study) for item in chunk]

            temp_responses = [
                await response
                for response in tqdm(
                    asyncio.as_completed(tasks),
                    total=len(tasks),
                    desc=f"Async Uploading {idx + 1}/{len(chunks)}",
                    file=sys.stdout,
                )
            ]
            responses = responses + temp_responses
    return responses


async def async_upload_study_data(item, client, study):
    """Coroutine to upload a single row of study data and handle the response."""
    feedback = copy.deepcopy(item["row"])
    url = (
        study.client.study_url
        + f"/record/{item['row']['record_id']}/data-point-collection/study"
    )
    json = {"common": item["common"], "data": item["body"]}
    feedback = await async_upload_data(client, feedback, json, study, url)
    return feedback


async def async_update_survey_data(data: list, study: "CastorStudy") -> list:
    """Updates the Castor EDC database with given survey datapoints."""
    # Split list to handle error when len(tasks) > max_connections
    chunks = [
        data[x : x + study.client.max_connections]
        for x in range(0, len(data), study.client.max_connections)
    ]
    responses = []
    for idx, chunk in enumerate(chunks):
        async with httpx.AsyncClient(
            headers=study.client.headers,
            timeout=study.client.timeout,
            limits=study.client.limits,
        ) as client:
            tasks = [async_upload_survey_data(item, client, study) for item in chunk]

            temp_responses = [
                await response
                for response in tqdm(
                    asyncio.as_completed(tasks),
                    total=len(tasks),
                    desc=f"Async Uploading {idx + 1}/{len(chunks)}",
                    file=sys.stdout,
                )
            ]
            responses = responses + temp_responses
    return responses


async def async_upload_survey_data(item, client, study):
    """Coroutine to upload a single row of survey package data to a new survey and handle the response."""
    feedback = copy.deepcopy(item["row"])
    try:
        instance = await async_create_survey_package_instance(
            survey_package_id=item["package_id"],
            record_id=item["row"]["record_id"],
            email_address=item["email"],
            auto_send=False,
            study=study,
            client=client,
        )
        body = create_survey_body(instance, item["row"], study)
        url = (
            study.client.study_url
            + f"/record/{item['row']['record_id']}/data-point-collection/"
            f"survey-package-instance/{instance['id']}"
        )
        json = {"data": body}
        feedback = await async_upload_data(client, feedback, json, study, url)
    except httpx.HTTPStatusError as error:
        feedback["error"] = error.response.json()
    return feedback


async def async_create_survey_package_instance(
    survey_package_id: str,
    record_id: str,
    email_address: str,
    auto_send: bool,
    study: "CastorStudy",
    client: httpx.AsyncClient,
):
    """Creates a survey package instance asynchronously."""
    url = study.client.study_url + "/surveypackageinstance"
    body = {
        "survey_package_id": survey_package_id,
        "record_id": record_id,
        "ccr_patient_id": None,
        "email_address": email_address,
        "package_invitation_subject": None,
        "package_invitation": None,
        "auto_send": auto_send,
        "auto_lock_on_finish": False,
    }
    response = await client.post(url=url, json=body)
    response.raise_for_status()
    return response.json()


async def async_update_report_data(data: list, study: "CastorStudy") -> list:
    """Updates the Castor EDC database with given report datapoints."""
    # Split list to handle error when len(tasks) > max_connections
    chunks = [
        data[x : x + study.client.max_connections]
        for x in range(0, len(data), study.client.max_connections)
    ]
    responses = []
    for idx, chunk in enumerate(chunks):
        async with httpx.AsyncClient(
            headers=study.client.headers,
            timeout=study.client.timeout,
            limits=study.client.limits,
        ) as client:
            tasks = [async_upload_report_data(item, client, study) for item in chunk]

            temp_responses = [
                await response
                for response in tqdm(
                    asyncio.as_completed(tasks),
                    total=len(tasks),
                    desc=f"Async Uploading {idx + 1}/{len(chunks)}",
                    file=sys.stdout,
                )
            ]
            responses = responses + temp_responses
    return responses


async def async_upload_report_data(item, client, study):
    """Coroutine to upload a single row of report data to a new report and handle the response."""
    feedback = copy.deepcopy(item["row"])
    try:
        instance = await async_create_report_instance(
            report_id=item["report_id"],
            record_id=item["row"]["record_id"],
            report_name_custom=item["report_name"],
            study=study,
            client=client,
        )
        body = create_report_body(instance, item["row"], study, item["upload_datetime"])
        url = (
            study.client.study_url
            + f"/record/{item['row']['record_id']}/data-point-collection/"
            f"report-instance/{instance['id']}"
        )
        json = {"data": body, "common": item["common"]}
        feedback = await async_upload_data(client, feedback, json, study, url)
    except httpx.HTTPStatusError as error:
        feedback["error"] = error.response.json()
    return feedback


async def async_create_report_instance(
    report_id: str,
    record_id: str,
    report_name_custom: str,
    study: "CastorStudy",
    client: httpx.AsyncClient,
):
    """Creates a survey package instance asynchronously."""
    url = study.client.study_url + f"/record/{record_id}/report-instance"
    body = {
        "report_id": report_id,
        "report_name_custom": report_name_custom,
        "parent_id": None,
    }
    response = await client.post(url=url, json=body)
    response.raise_for_status()
    return response.json()


async def async_upload_data(client, feedback, json, study, url):
    """Sends body to url and awaits response"""
    response = await client.post(url=url, json=json)
    try:
        response.raise_for_status()
        from castoredc_api.importer.helpers import format_feedback

        formatted_response = format_feedback(response.json(), study)
        feedback["error"] = None
        feedback["success"] = formatted_response["success"]
        feedback["failed"] = formatted_response["failed"]
    except HTTPStatusError as error:
        feedback["error"] = error.response.json()
        feedback["success"] = None
        feedback["failed"] = None
    return feedback
