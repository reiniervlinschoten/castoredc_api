"""Helper functions for uploading data asynchronously"""
import asyncio
import copy
import typing
from json import JSONDecodeError

import httpx
from tqdm import tqdm

from castoredc_api.importer.helpers import (
    create_survey_body,
    create_report_body,
    format_feedback,
)

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
    # Create a new client for each chunk because of problem when tasks > max_connections
    for idx, chunk in enumerate(chunks):
        async with httpx.AsyncClient(
            headers=study.client.headers,
            timeout=study.client.timeout,
            limits=study.client.limits,
        ) as client:
            tasks = [async_upload_study_data(item, client, study) for item in chunk]

            # Show progress bar while running tasks
            temp_responses = [
                await response
                for response in tqdm(
                    asyncio.as_completed(tasks),
                    total=len(tasks),
                    desc=f"Async Uploading {idx + 1}/{len(chunks)}",
                )
            ]
            responses = responses + temp_responses
    return responses


async def async_upload_study_data(item, client, study):
    """Coroutine to upload a single row of study data and handle the response."""
    feedback = copy.deepcopy(item["row"])
    try:
        # Copy row because we don't want to overwrite dict
        url = (
            study.client.study_url
            + f"/record/{item['row']['record_id']}/data-point-collection/study"
        )
        json = {"common": item["common"], "data": item["body"]}
        feedback = await async_upload_data(client, feedback, json, study, url)
    except httpx.HTTPStatusError as error:
        feedback["error"] = error.response.json()
    except httpx.RequestError as error:
        feedback["error"] = f"Request Error for {error.request.url}."
    except JSONDecodeError:
        feedback["error"] = "JSONDecodeError while handling Error."
    return feedback


async def async_update_survey_data(
    data: list, study: "CastorStudy", change_reason: str
) -> list:
    """Updates the Castor EDC database with given survey datapoints."""
    # Split list to handle error when len(tasks) > max_connections
    chunks = [
        data[x : x + study.client.max_connections]
        for x in range(0, len(data), study.client.max_connections)
    ]
    responses = []
    # Create a new client for each chunk because of problem when tasks > max_connections
    for idx, chunk in enumerate(chunks):
        async with httpx.AsyncClient(
            headers=study.client.headers,
            timeout=study.client.timeout,
            limits=study.client.limits,
        ) as client:
            tasks = [
                async_upload_survey_data(item, client, study, change_reason)
                for item in chunk
            ]

            # Show progress bar when handling responses
            temp_responses = [
                await response
                for response in tqdm(
                    asyncio.as_completed(tasks),
                    total=len(tasks),
                    desc=f"Async Uploading {idx + 1}/{len(chunks)}",
                )
            ]
            responses = responses + temp_responses
    return responses


async def async_upload_survey_data(item, client, study, change_reason):
    """Coroutine to upload a single row of survey data to a new survey and handle the response."""
    # Copy so we don't overwrite dict
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
        json = {"data": body, "common": {"change_reason": change_reason}}
        feedback = await async_upload_data(client, feedback, json, study, url)
    except httpx.HTTPStatusError as error:
        feedback["error"] = error.response.json()
    except httpx.RequestError as error:
        feedback["error"] = f"Request Error for {error.request.url}."
    except JSONDecodeError:
        feedback["error"] = "JSONDecodeError while handling Error."
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
    # Create a new client for each chunk because of problem when tasks > max_connections
    for idx, chunk in enumerate(chunks):
        async with httpx.AsyncClient(
            headers=study.client.headers,
            timeout=study.client.timeout,
            limits=study.client.limits,
        ) as client:
            tasks = [async_upload_report_data(item, client, study) for item in chunk]

            # Show progress bar while handling responses
            temp_responses = [
                await response
                for response in tqdm(
                    asyncio.as_completed(tasks),
                    total=len(tasks),
                    desc=f"Async Uploading {idx + 1}/{len(chunks)}",
                )
            ]
            responses = responses + temp_responses
    return responses


async def async_upload_report_data(item, client, study):
    """Coroutine to upload a single row of report data to a new report and handle the response."""
    # Copy because we don't want to overwrite dict
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
    except httpx.RequestError as error:
        feedback["error"] = f"Request Error for {error.request.url}."
    except JSONDecodeError:
        feedback["error"] = "JSONDecodeError while handling Error."
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
    response.raise_for_status()
    formatted_response = format_feedback(response.json(), study)
    feedback["success"] = formatted_response["success"]
    feedback["failed"] = formatted_response["failed"]
    return feedback
