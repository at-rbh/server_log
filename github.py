
def server_log(filename):
    try:
        with open(filename, "r") as file:
            data = [line.strip() for line in file.readlines()]
            return data
    except FileNotFoundError:
        print("File not found")
        return []


def log_count(server_data):
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for line in server_data:
        parts = line.split()
        if len(parts) >= 3:
            level = parts[2]
            if level in line:
                counts[level] += 1
    return counts


def frequency(server_data):
    freq = {}
    for line in server_data:
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) > 2:
            level = line.split()[2]
            if level == "ERROR":
                message = line.split(level, 1)[1].strip()
                if message not in freq:
                    freq[message] = 1
                else:
                    freq[message] += 1
    return freq


def error_peak_hour(server_data):
    error_count = {}

    for line in server_data:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[2] == "ERROR":
            hour = int(parts[1].split(":")[0])
            error_count[hour] = error_count.get(
                hour, 0) + 1

    if not error_count:
        return {}

    max_hours = max(error_count, key=error_count.get)
    return {
        f"{max_hours}:00 - {max_hours}:59": error_count[max_hours]
    }


def save_file(log, freq, error):
    with open("server.txt", "w") as file:
        file.write("All log file count\n")
        for message, count in log.items():
            file.write(f"{message}: {count}\n")

        file.write("\nfrequency error data\n")
        for message, count in freq.items():

            file.write(f"{message}: {count}\n")

        file.write("\nError peak hour\n")
        for time, count in error.items():
            file.write(f"{time}: {count}\n")


raw_data = server_log("server.log")
log = log_count(raw_data)
freq = frequency(raw_data)
error = error_peak_hour(raw_data)
save_file(log, freq, error)
