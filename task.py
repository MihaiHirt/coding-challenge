import re
from datetime import datetime
import time

pattern = r"^(\d{2}:\d{2}:\d{2}),(scheduled task|background job) ([\w\d]+), (START|END),(\d+)"

tasks = {}

results = []

with open("logs.log", "r") as file:
    for line in file:
        match = re.match(pattern, line.strip())
        if match:
            timestamp_str, task_type, task_id, action, pid = match.groups()
            timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
            key = (task_type, task_id, pid)

            if action == "START":
                tasks[key] = timestamp
            elif action == "END":
                start_time = tasks.pop(key, None)
                if start_time:
                    duration = (timestamp - start_time).total_seconds()

                    if duration <= 300:
                        status = "OK"
                    elif duration > 300 and duration <= 600:
                        status = "WARNING"
                    else:
                        status = "ERROR"


                    if duration > 300:
                        results.append({
                        "type": task_type,
                        "id": task_id,
                        "pid": pid,
                        "duration": int(duration),
                        "duration in mins": time.strftime("%H:%M:%S", time.gmtime(duration)),
                        "status": status,
                        "start_time": start_time,
                        "end_time": timestamp,
                    })


for r in results:
        print(f"{r['status']} : {r['type']} {r['id']} (PID {r['pid']}) ran for {r['duration']} seconds -- {r['duration in mins']} minutes")

