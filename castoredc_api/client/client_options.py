"""File to hold settings for interacting with the Castor EDC API."""

import time
import httpx

MAX_CONNECTIONS = 15
TIMEOUT = httpx.Timeout(10.0, read=60)
LIMITS = httpx.Limits(max_connections=MAX_CONNECTIONS)
# Rate limit is 600 calls per 10 minutes per api endpoint
SYNC_LIMIT = 600
PERIOD_LIMIT = 600
ASYNC_LIMIT = SYNC_LIMIT / MAX_CONNECTIONS


def limit_callback(until):
    """Returns time until rate limitation ends"""
    duration = int(round(until - time.time()))
    print(f"Rate limited, sleeping for {duration} seconds")


SYNC_OPTIONS = {
    "max_calls": SYNC_LIMIT,
    "period": PERIOD_LIMIT,
    "callback": limit_callback,
}
