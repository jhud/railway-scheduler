import schedule
import time
import json
import os

import job_http_request

import sentry_sdk

# Catch errors with Sentry
sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

"""
Be aware that it runs at UTC on Railway.
Example of how to run this service:
SCHEDULE=[{"time":"08:30", "job": "get", "param": "https://www.google.com/api/foo/"}] python main.py
"""

jobs = {"get": job_http_request.job_get, "post": job_http_request.job_post}

sched = json.loads(os.environ["SCHEDULE"])

for action in sched:
    timing = action["time"]
    param = action["param"]

    print(f"   Scheduling {action['job']} at {timing}, param ...{param[-20:]}")

    job_exec = jobs[action["job"]]

    try:
        if timing == "test":
            schedule.every(10).seconds.do(job_exec, param)
        elif timing == "frequent":
            schedule.every(10).minutes.do(job_exec, param)
        elif timing == "hourly":
            schedule.every().hour.do(job_exec, param)
        elif timing == "never":
            pass
        else:
            schedule.every().day.at(timing).do(job_exec, action["param"])
    except job_http_request.JobFailedException as e:
        print("Logging failure of job with Sentry...")
        sentry_sdk.capture_exception(e)

while True:
    schedule.run_pending()
    time.sleep(int(os.getenv("POLL_SECONDS", 3600)))
