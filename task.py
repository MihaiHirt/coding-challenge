def parse_log_file(filename):
    import re
    from datetime import datetime
    import time

    # regex pattern for parsing
    pattern = r"^(\d{2}:\d{2}:\d{2}),(scheduled task|background job) ([\w\d]+), (START|END),(\d+)"

    # store start timestamps
    tasks = {}

    # store results
    results = []

    # open and read log file
    with open(filename, "r") as file:
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                timestamp_str, task_type, task_id, action, pid = match.groups()
                # duration calculation
                timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
                key = (task_type, task_id, pid)

                # verify the pattern for each log entry and store the timestamp
                if action == "START":
                    tasks[key] = timestamp
                elif action == "END":
                    start_time = tasks.pop(key, None)
                    if start_time:
                        duration = (timestamp - start_time).total_seconds()

                        # Categorize duration
                        if duration <= 300:
                            status = "OK"
                        elif duration > 300 and duration <= 600:
                            status = "WARNING"
                        else:
                            status = "ERROR"

                        # store the results in a list of dictionaries
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

    # output results
    # for r in results:
    #         print(f"{r['status']} : {r['type']} {r['id']} (PID {r['pid']}) ran for {r['duration']} seconds -- {r['duration in mins']} minutes")

    # other way for printing
    # for r in results:
    #     print(f"[{r['status']}] Job '{r['type']}' with PID {r['pid']} ran from {r['start_time'].time()} to {r['end_time'].time()} taking {r['duration']} seconds -- {r['duration in mins']} minutes.")

    # output results to console and file
    with open("output.txt", "w") as out_file:
        for r in results:
            line = (f"{r['status']} : {r['type']} {r['id']} (PID {r['pid']}) ran for {r['duration']} seconds -- {r['duration in mins']} minutes")
            print(line)
            out_file.write(line + "\n")

    return results

if __name__ == '__main__':
    parse_log_file("logs.log")