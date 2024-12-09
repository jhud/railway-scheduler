import schedule
import time
import json
import os

import job_http_request

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

while True:
    schedule.run_pending()
    time.sleep(int(os.getenv("POLL_SECONDS", 3600)))
